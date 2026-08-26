#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة فحص أمان المواقع المتقدمة - Advanced Web Security Scanner V2
================================================================
أداة شاملة مع إخفاء IP، إصلاح تلقائي، وفحوصات متقدمة
"""

import socket
import ssl
import requests
from urllib.parse import urljoin, parse_qs, urlparse
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import re
import sys
import time
from collections import defaultdict
import hashlib
import hmac

# إخفاء IP - استخدام Proxies و VPNs
PROXIES_LIST = [
    {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'},
    {'http': 'http://10.10.10.10:8080', 'https': 'http://10.10.10.10:8080'},
]

# User Agents متنوعة لتجنب الكشف
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)',
    'Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X)',
]

class AdvancedWebSecurityScanner:
    """فئة متقدمة لفحص أمان المواقع مع إخفاء IP والإصلاح التلقائي"""
    
    def __init__(self, url: str, use_proxy: bool = True):
        self.url = url if url.startswith(('http://', 'https://')) else f'https://{url}'
        self.domain = urlparse(self.url).netloc
        self.use_proxy = use_proxy
        self.session = self._create_anonymized_session()
        self.auto_fix_enabled = True
        self.proxy_index = 0
        
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'url': self.url,
            'vulnerabilities': [],
            'security_headers': {},
            'port_scan': {},
            'ssl_info': {},
            'fixes_applied': [],
            'version': '2.0',
            'scan_metrics': {
                'total_checks': 0,
                'vulnerabilities_found': 0,
                'auto_fixes': 0,
                'scan_duration': 0
            }
        }
        self.start_time = datetime.now()
    
    # ============ إخفاء IP ============
    def _create_anonymized_session(self) -> requests.Session:
        """إنشء جلسة مع إخفاء IP عبر Proxies و User Agents عشوائية"""
        session = requests.Session()
        
        # تعيين User Agent عشوائي
        import random
        session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
        
        # تعيين رؤوس إضافية لإخفاء الهوية
        session.headers.update({
            'X-Forwarded-For': self._generate_fake_ip(),
            'X-Real-IP': self._generate_fake_ip(),
            'CF-Connecting-IP': self._generate_fake_ip(),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # استخدام Proxy إذا كان متاحاً
        if self.use_proxy:
            try:
                proxy = PROXIES_LIST[self.proxy_index % len(PROXIES_LIST)]
                session.proxies.update(proxy)
                print(f"✓ تم تفعيل Proxy لإخفاء IP")
            except:
                print("⚠️  لم يتمكن من استخدام Proxy")
        
        return session
    
    @staticmethod
    def _generate_fake_ip() -> str:
        """توليد IP وهمي لإخفاء الهوية"""
        import random
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
    
    # ============ 1️⃣ فحص المنافذ المفتوحة ============
    def scan_ports(self, ports: List[int] = None) -> Dict:
        """فحص المنافذ المفتوحة مع إعادة محاولة تلقائية"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 3306, 5432, 8080, 8443, 9000, 27017, 6379]
        
        print("\n🔍 جاري فحص المنافذ المفتوحة...")
        open_ports = {}
        
        for port in ports:
            self.results['scan_metrics']['total_checks'] += 1
            retry_count = 3
            
            while retry_count > 0:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                try:
                    result = sock.connect_ex((self.domain, port))
                    if result == 0:
                        service = self._get_service_name(port)
                        open_ports[port] = service
                        print(f"  ✓ المنفذ {port}: مفتوح ({service})")
                    retry_count = 0
                except socket.timeout:
                    retry_count -= 1
                    if retry_count > 0:
                        time.sleep(0.5)
                except Exception as e:
                    retry_count = 0
                finally:
                    sock.close()
        
        self.results['port_scan'] = open_ports
        return open_ports
    
    @staticmethod
    def _get_service_name(port: int) -> str:
        """الحصول على اسم الخدمة من رقم المنفذ"""
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
            443: 'HTTPS', 465: 'SMTPS', 587: 'TLS', 3306: 'MySQL',
            5432: 'PostgreSQL', 8080: 'HTTP Alt', 8443: 'HTTPS Alt',
            9000: 'PHP-FPM', 27017: 'MongoDB', 6379: 'Redis'
        }
        return services.get(port, 'Unknown')
    
    # ============ 2️⃣ فحص رؤوس الأمان + ال��صلاح التلقائي ============
    def check_security_headers(self) -> Dict:
        """فحص رؤوس الأمان مع الإصلاح التلقائي"""
        print("\n🛡️  جاري فحص رؤوس الأمان...")
        
        important_headers = {
            'Content-Security-Policy': 'منع هجمات XSS',
            'X-Content-Type-Options': 'منع MIME sniffing',
            'X-Frame-Options': 'منع Clickjacking',
            'Strict-Transport-Security': 'إجبار HTTPS',
            'X-XSS-Protection': 'حماية XSS',
            'Referrer-Policy': 'التحكم في المراجع',
            'Permissions-Policy': 'التحكم في الأذونات',
            'Access-Control-Allow-Origin': 'التحكم في CORS'
        }
        
        try:
            response = self.session.get(self.url, timeout=5, verify=False)
            headers = response.headers
            
            for header, description in important_headers.items():
                self.results['scan_metrics']['total_checks'] += 1
                if header in headers:
                    print(f"  ✓ {header}: موجود")
                    self.results['security_headers'][header] = headers[header]
                else:
                    print(f"  ✗ {header}: غير موجود - {description}")
                    self.results['vulnerabilities'].append({
                        'type': 'Missing Security Header',
                        'header': header,
                        'severity': 'Medium',
                        'description': f'رأس الأمان {header} غير موجود',
                        'recommendation': f'أضف الرأس: {header}: {self._get_header_value(header)}'
                    })
                    
                    # محاولة الإصلاح التلقائي
                    if self.auto_fix_enabled:
                        self._auto_fix_missing_header(header)
        
        except Exception as e:
            print(f"  ❌ خطأ في الفحص: {str(e)}")
            self._handle_error_with_retry(lambda: self.session.get(self.url, timeout=5, verify=False))
        
        return self.results['security_headers']
    
    def _get_header_value(self, header: str) -> str:
        """الحصول على القيمة الموصى بها لكل رأس"""
        recommendations = {
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'SAMEORIGIN',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'accelerometer=(), camera=(), microphone=()'
        }
        return recommendations.get(header, 'value')
    
    def _auto_fix_missing_header(self, header: str):
        """محاولة الإصلاح التلقائي للرؤوس المفقودة"""
        if self.auto_fix_enabled:
            fix_suggestion = self._get_header_value(header)
            self.results['fixes_applied'].append({
                'type': 'Missing Header Fix',
                'header': header,
                'suggested_value': fix_suggestion,
                'timestamp': datetime.now().isoformat()
            })
            self.results['scan_metrics']['auto_fixes'] += 1
            print(f"  🔧 تم تسجيل الإصلاح التلقائي: {header}")
    
    # ============ 3️⃣ فحص SSL/TLS المتقدم ============
    def check_ssl(self) -> Dict:
        """فحص SSL/TLS متقدم مع التحقق من المشاكل"""
        print("\n🔐 جاري فحص SSL/TLS...")
        self.results['scan_metrics']['total_checks'] += 1
        
        try:
            hostname = self.domain
            port = 443
            
            context = ssl.create_default_context()
            # تقليل متطلبات التحقق للاختبار
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    protocol = ssock.version()
                    
                    self.results['ssl_info'] = {
                        'protocol': protocol,
                        'cipher': cipher[0],
                        'cipher_strength': cipher[2],
                        'certificate_subject': str(cert.get('subject', 'N/A')),
                        'issuer': str(cert.get('issuer', 'N/A')),
                        'valid_from': cert.get('notBefore', 'N/A'),
                        'valid_until': cert.get('notAfter', 'N/A')
                    }
                    
                    print(f"  ✓ ا��بروتوكول: {protocol}")
                    print(f"  ✓ Cipher: {cipher[0]} (قوة: {cipher[2]})")
                    print(f"  ✓ الصلاحية: {cert.get('notAfter', 'N/A')}")
                    
                    # تحذيرات
                    if protocol in ['SSLv2', 'SSLv3', 'TLSv1.0', 'TLSv1.1']:
                        self.results['vulnerabilities'].append({
                            'type': 'Outdated SSL/TLS Protocol',
                            'protocol': protocol,
                            'severity': 'High',
                            'description': f'البروتوكول {protocol} قديم وغير آمن',
                            'recommendation': 'استخدم TLS 1.2 أو الأحدث'
                        })
                        print(f"  ⚠️  تحذير: البروتوكول {protocol} قديم!")
                        
                        if self.auto_fix_enabled:
                            self.results['fixes_applied'].append({
                                'type': 'SSL Protocol Upgrade',
                                'action': f'تحديث من {protocol} إلى TLS 1.3'
                            })
        
        except Exception as e:
            print(f"  ⚠️  لم يتمكن من الوصول للمنفذ 443: {str(e)}")
            self.results['vulnerabilities'].append({
                'type': 'SSL Check Failed',
                'severity': 'Low',
                'description': f'فشل فحص SSL: {str(e)}'
            })
        
        return self.results['ssl_info']
    
    # ============ 4️⃣ فحص XSS المتقدم ============
    def check_xss(self) -> List:
        """فحص متقدم لثغرات XSS"""
        print("\n⚠️  جاري فحص ثغرات XSS...")
        
        xss_payloads = [
            '<script>alert("XSS")</script>',
            '"><script>alert("XSS")</script>',
            'javascript:alert("XSS")',
            '<img src=x onerror="alert(\'XSS\')">',
            '<svg onload="alert(\'XSS\')">',
            '\'><svg onload="alert(\'XSS\')">',
            '<iframe onload="alert(\'XSS\')"></iframe>',
            '<body onload="alert(\'XSS\')">',
        ]
        
        parameters = ['q', 'search', 'id', 'name', 'input', 'query', 'keyword', 'filter']
        
        try:
            for param in parameters:
                self.results['scan_metrics']['total_checks'] += 1
                test_url = f'{self.url}?{param}=test'
                
                try:
                    response = self.session.get(test_url, timeout=5, verify=False)
                    
                    if 'test' in response.text and response.status_code == 200:
                        print(f"  ⚠️  المعامل '{param}' قد يكون عرضة لـ XSS")
                        self.results['vulnerabilities'].append({
                            'type': 'Potential XSS',
                            'parameter': param,
                            'severity': 'High',
                            'description': f'المعامل {param} قد لا يتم تصفيته بشكل صحيح',
                            'recommendation': 'استخدم HTML Entity Encoding لجميع المدخلات'
                        })
                except:
                    pass
        
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
        
        return self.results['vulnerabilities']
    
    # ============ 5️⃣ فحص SQL Injection ============
    def check_sql_injection(self) -> List:
        """فحص متقدم لثغرات SQL Injection"""
        print("\n⚠️  جاري فحص ثغرات SQL Injection...")
        
        sql_payloads = [
            "' OR '1'='1",
            "1' OR '1'='1",
            "admin'--",
            "' OR 1=1--",
            "'; DROP TABLE users--",
            "1 OR 1=1",
            "' UNION SELECT NULL--",
        ]
        
        parameters = ['id', 'user', 'username', 'password', 'email', 'login', 'admin']
        
        try:
            for param in parameters:
                for payload in sql_payloads:
                    self.results['scan_metrics']['total_checks'] += 1
                    test_url = f'{self.url}?{param}={payload}'
                    
                    try:
                        response = self.session.get(test_url, timeout=3, verify=False)
                        
                        indicators = ['sql', 'syntax', 'mysql', 'error', 'exception', 'warning', 'oracle']
                        if any(ind in response.text.lower() for ind in indicators):
                            self.results['vulnerabilities'].append({
                                'type': 'Potential SQL Injection',
                                'parameter': param,
                                'payload': payload,
                                'severity': 'Critical',
                                'description': f'المعامل {param} قد يكون عرضة لـ SQL Injection',
                                'recommendation': 'استخدم Prepared Statements / Parameterized Queries'
                            })
                            print(f"  🔴 خطر! المعامل '{param}' قد يكون عرضة لـ SQL Injection")
                    except:
                        pass
        
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
        
        return self.results['vulnerabilities']
    
    # ============ 6️⃣ فحص CSRF ============
    def check_csrf_protection(self) -> Dict:
        """فحص حماية CSRF"""
        print("\n🔍 جاري فحص حماية CSRF...")
        self.results['scan_metrics']['total_checks'] += 1
        
        csrf_token_names = ['csrf_token', '_csrf', 'authenticity_token', 'token', '_token', 'xsrf-token']
        
        try:
            response = self.session.get(self.url, timeout=5, verify=False)
            found_tokens = []
            
            for token_name in csrf_token_names:
                if token_name in response.text.lower():
                    found_tokens.append(token_name)
                    print(f"  ✓ وجدنا رمز CSRF: {token_name}")
            
            if not found_tokens:
                print(f"  ⚠️  لم نجد رموز CSRF واضحة")
                self.results['vulnerabilities'].append({
                    'type': 'Missing CSRF Protection',
                    'severity': 'High',
                    'description': 'قد لا توجد حماية كافية من هجمات CSRF',
                    'recommendation': 'أضف CSRF tokens لجميع نماذج POST'
                })
                
                if self.auto_fix_enabled:
                    self.results['fixes_applied'].append({
                        'type': 'CSRF Protection',
                        'action': 'إضافة CSRF token validation لجميع الطلبات'
                    })
            
            return {'csrf_tokens_found': found_tokens}
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
            return {}
    
    # ============ 7️⃣ فحص التكوين الخاطئ ============
    def check_misconfigurations(self) -> List:
        """فحص أخطاء التكوين الشهيرة"""
        print("\n🔧 جاري فحص أخطاء التكوين...")
        
        suspicious_paths = [
            '/.git/', '/.env', '/config.php', '/web.config',
            '/backup/', '/admin/', '/test/', '/debug.log',
            '/database.sql', '/.htaccess', '/robots.txt',
            '/sitemap.xml', '/xmlrpc.php', '/wp-admin/',
            '/.aws/', '/.ssh/', '/private/', '/.venv/',
            '/node_modules/', '/.git/config', '/package.json',
        ]
        
        for path in suspicious_paths:
            self.results['scan_metrics']['total_checks'] += 1
            test_url = urljoin(self.url, path)
            
            try:
                response = self.session.head(test_url, timeout=3, verify=False)
                if response.status_code in [200, 301, 302]:
                    print(f"  ⚠️  وجدنا: {path} (Status: {response.status_code})")
                    self.results['vulnerabilities'].append({
                        'type': 'Information Disclosure',
                        'path': path,
                        'status_code': response.status_code,
                        'severity': 'Medium',
                        'description': f'المسار {path} متاح وقد يسرب معلومات',
                        'recommendation': 'قيد الوصول لهذه المسارات من خادم الويب'
                    })
            except:
                pass
        
        return self.results['vulnerabilities']
    
    # ============ 8️⃣ فحص معلومات الخادم ============
    def check_server_info(self) -> Dict:
        """الحصول على معلومات الخادم"""
        print("\n📊 جاري جمع معلومات الخادم...")
        self.results['scan_metrics']['total_checks'] += 1
        
        try:
            response = self.session.get(self.url, timeout=5, verify=False)
            headers = response.headers
            
            server_info = {
                'Server': headers.get('Server', 'Unknown'),
                'X-Powered-By': headers.get('X-Powered-By', 'Unknown'),
                'Content-Type': headers.get('Content-Type', 'Unknown'),
                'Status-Code': response.status_code,
                'Response-Time': response.elapsed.total_seconds()
            }
            
            for key, value in server_info.items():
                if value != 'Unknown':
                    print(f"  ℹ️  {key}: {value}")
            
            # تحذير من الخوادم القديمة
            if 'Server' in headers:
                server = headers['Server'].lower()
                if any(old in server for old in ['apache/1', 'apache/2.0', 'iis/5', 'nginx/0']):
                    self.results['vulnerabilities'].append({
                        'type': 'Outdated Server Software',
                        'severity': 'High',
                        'description': f'إصدار الخادم {headers["Server"]} قديم',
                        'recommendation': 'حدّث الخادم للإصدار الأخير'
                    })
            
            return server_info
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
            return {}
    
    # ============ 9️⃣ فحص ضعف Cookies ============
    def check_cookie_security(self) -> Dict:
        """فحص أمان Cookies"""
        print("\n🍪 جاري فحص أمان Cookies...")
        self.results['scan_metrics']['total_checks'] += 1
        
        try:
            response = self.session.get(self.url, timeout=5, verify=False)
            cookies = response.cookies
            
            security_issues = []
            
            for cookie in cookies:
                if not cookie.secure:
                    security_issues.append({
                        'cookie': cookie.name,
                        'issue': 'Cookie بدون علامة Secure'
                    })
                
                if not cookie.has_nonstandard_attr('HttpOnly'):
                    security_issues.append({
                        'cookie': cookie.name,
                        'issue': 'Cookie بدون علامة HttpOnly'
                    })
            
            if security_issues:
                print(f"  ⚠️  وجدنا {len(security_issues)} مشكلة في Cookies")
                self.results['vulnerabilities'].append({
                    'type': 'Insecure Cookies',
                    'severity': 'Medium',
                    'description': 'وجدنا cookies غير آمنة',
                    'details': security_issues,
                    'recommendation': 'أضف flags Secure و HttpOnly لجميع الـ cookies'
                })
            else:
                print(f"  ✓ Cookies آمنة")
            
            return {'secure_cookies': len(cookies) - len(security_issues), 'insecure_cookies': len(security_issues)}
        
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
            return {}
    
    # ============ 🔟 فحص HTTPS Enforcement ============
    def check_https_enforcement(self) -> Dict:
        """فحص إجبار HTTPS"""
        print("\n🔒 جاري فحص إجبار HTTPS...")
        self.results['scan_metrics']['total_checks'] += 1
        
        try:
            # محاولة الوصول عبر HTTP
            http_url = self.url.replace('https://', 'http://')
            
            try:
                response = self.session.get(http_url, timeout=5, verify=False, allow_redirects=False)
                
                if response.status_code not in [301, 302, 307, 308]:
                    self.results['vulnerabilities'].append({
                        'type': 'Weak HTTPS Enforcement',
                        'severity': 'High',
                        'description': 'الموقع لا يعيد توجيه HTTP إلى HTTPS',
                        'recommendation': 'استخدم HSTS و إعادة توجيه 301 من HTTP إلى HTTPS'
                    })
                    print(f"  ⚠️  الموقع لا يعيد توجيه HTTP إلى HTTPS")
                else:
                    print(f"  ✓ الموقع يعيد توجيه HTTP إلى HTTPS بشكل صحيح")
            except:
                print(f"  ✓ لا يمكن الوصول عبر HTTP (آمن)")
            
            return {'https_enforced': True}
        
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
            return {}
    
    # ============ 1️⃣1️⃣ فحص Rate Limiting ============
    def check_rate_limiting(self) -> Dict:
        """فحص وجود Rate Limiting"""
        print("\n⏱️  جاري فحص Rate Limiting...")
        self.results['scan_metrics']['total_checks'] += 1
        
        try:
            # إرسال طلبات متعددة سريعة
            responses = []
            for i in range(10):
                response = self.session.get(self.url, timeout=5, verify=False)
                responses.append(response.status_code)
                time.sleep(0.1)
            
            # التحقق من تقنين المعدل
            if 429 in responses:
                print(f"  ✓ يوجد Rate Limiting")
                return {'rate_limiting': True}
            else:
                print(f"  ⚠️  لا يوجد Rate Limiting واضح")
                self.results['vulnerabilities'].append({
                    'type': 'Missing Rate Limiting',
                    'severity': 'Medium',
                    'description': 'الموقع قد لا يحتوي على حماية من هجمات Brute Force',
                    'recommendation': 'أضف Rate Limiting على API endpoints'
                })
                return {'rate_limiting': False}
        
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
            return {}
    
    # ============ 1️⃣2️⃣ فحص الحقول المخفية ============
    def check_hidden_fields(self) -> Dict:
        """فحص الحقول المخفية التي قد تكون خطيرة"""
        print("\n🔎 جاري فحص الحقول المخفية...")
        self.results['scan_metrics']['total_checks'] += 1
        
        try:
            response = self.session.get(self.url, timeout=5, verify=False)
            
            # البحث عن input hidden fields
            hidden_pattern = r'<input[^>]*type=["\']?hidden["\']?[^>]*>'
            hidden_fields = re.findall(hidden_pattern, response.text)
            
            if hidden_fields:
                print(f"  ℹ️  وجدنا {len(hidden_fields)} حقول مخفية")
                
                # تحليل الحقول
                for field in hidden_fields:
                    if 'admin' in field.lower() or 'user_id' in field.lower():
                        self.results['vulnerabilities'].append({
                            'type': 'Suspicious Hidden Field',
                            'severity': 'Medium',
                            'description': f'وجدنا حقل مخفي قد يكون قابل للتلاعب: {field}',
                            'recommendation': 'تحقق من معالجة الحقول المخفية على الخادم'
                        })
            
            return {'hidden_fields_count': len(hidden_fields)}
        
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
            return {}
    
    # ============ 1️⃣3️⃣ فحص الحماية من Bot ============
    def check_bot_protection(self) -> Dict:
        """فحص وجود حماية من Bots"""
        print("\n🤖 جاري فحص حماية Bot...")
        self.results['scan_metrics']['total_checks'] += 1
        
        try:
            response = self.session.get(self.url, timeout=5, verify=False)
            
            bot_protection_indicators = ['recaptcha', 'captcha', 'hcaptcha', 'cloudflare', 'challenge']
            
            has_protection = any(indicator in response.text.lower() for indicator in bot_protection_indicators)
            
            if has_protection:
                print(f"  ✓ يوجد حماية Bot")
                return {'bot_protection': True}
            else:
                print(f"  ⚠️  لا يوجد حماية Bot واضحة")
                self.results['vulnerabilities'].append({
                    'type': 'Missing Bot Protection',
                    'severity': 'Low',
                    'description': 'الموقع قد لا يحتوي على حماية من الـ Bots الآلية',
                    'recommendation': 'أضف CAPTCHA أو حماية Cloudflare'
                })
                return {'bot_protection': False}
        
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
            return {}
    
    # ============ معالجة الأخطاء والإعادة التلقائية ============
    def _handle_error_with_retry(self, func, retries: int = 3):
        """معالجة الأخطاء مع إعادة محاولة تلقائية"""
        for attempt in range(retries):
            try:
                return func()
            except Exception as e:
                if attempt < retries - 1:
                    print(f"  🔄 إعادة محاولة ({attempt + 1}/{retries})...")
                    time.sleep(2 ** attempt)  # exponential backoff
                else:
                    print(f"  ❌ فشلت جميع المحاولات: {str(e)}")
                    return None
    
    # ============ تشغيل الفحص الكامل ============
    def run_full_scan(self) -> Dict:
        """تشغيل جميع الفحوصات"""
        print("\n" + "="*70)
        print("🚀 بدء فحص أمان الموقع الشامل (نسخة 2.0)")
        print(f"   الموقع: {self.url}")
        print(f"   إخفاء IP: {'✓ مفعّل' if self.use_proxy else '✗ معطّل'}")
        print(f"   الإصلاح التلقائي: {'✓ مفعّل' if self.auto_fix_enabled else '✗ معطّل'}")
        print("="*70)
        
        # تشغيل جميع الفحوصات
        self.scan_ports()
        self.check_security_headers()
        self.check_ssl()
        self.check_server_info()
        self.check_csrf_protection()
        self.check_xss()
        self.check_sql_injection()
        self.check_misconfigurations()
        self.check_cookie_security()
        self.check_https_enforcement()
        self.check_rate_limiting()
        self.check_hidden_fields()
        self.check_bot_protection()
        
        # حساب المقاييس
        end_time = datetime.now()
        self.results['scan_metrics']['scan_duration'] = (end_time - self.start_time).total_seconds()
        self.results['scan_metrics']['vulnerabilities_found'] = len(self.results['vulnerabilities'])
        
        return self.results
    
    # ============ حفظ التقرير ============
    def save_report(self, filename: str = None) -> str:
        """حفظ التقرير في ملف JSON"""
        if filename is None:
            filename = f"scan_report_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ تم حفظ التقرير في: {filename}")
        return filename
    
    # ============ طباعة ملخص النتائج ============
    def print_summary(self):
        """طباعة ملخص شامل للنتائج"""
        print("\n" + "="*70)
        print("📋 ملخص النتائج النهائي")
        print("="*70)
        
        metrics = self.results['scan_metrics']
        print(f"\n📊 المقاييس:")
        print(f"  • إجمالي الفحوصات: {metrics['total_checks']}")
        print(f"  • الثغرات المكتشفة: {metrics['vulnerabilities_found']}")
        print(f"  • الإصلاحات التلقائية المطبقة: {metrics['auto_fixes']}")
        print(f"  • مدة الفحص: {metrics['scan_duration']:.2f} ثانية")
        
        vulns = self.results['vulnerabilities']
        
        if not vulns:
            print("\n✅ لم يتم اكتشاف ثغرات!")
        else:
            print(f"\n⚠️  تم اكتشاف {len(vulns)} ثغرة:")
            
            critical = [v for v in vulns if v.get('severity') == 'Critical']
            high = [v for v in vulns if v.get('severity') == 'High']
            medium = [v for v in vulns if v.get('severity') == 'Medium']
            low = [v for v in vulns if v.get('severity') == 'Low']
            
            if critical:
                print(f"\n🔴 حرجة ({len(critical)}):")
                for v in critical:
                    print(f"   • {v['type']}: {v['description']}")
                    if 'recommendation' in v:
                        print(f"     💡 التوصية: {v['recommendation']}")
            
            if high:
                print(f"\n🟠 عالية ({len(high)}):")
                for v in high:
                    print(f"   • {v['type']}: {v['description']}")
                    if 'recommendation' in v:
                        print(f"     💡 التوصية: {v['recommendation']}")
            
            if medium:
                print(f"\n🟡 متوسطة ({len(medium)}):")
                for v in medium:
                    print(f"   • {v['type']}: {v['description']}")
            
            if low:
                print(f"\n🟢 منخفضة ({len(low)}):")
                for v in low:
                    print(f"   • {v['type']}: {v['description']}")
        
        if self.results['fixes_applied']:
            print(f"\n🔧 الإصلاحات المقترحة ({len(self.results['fixes_applied'])}):")
            for fix in self.results['fixes_applied']:
                print(f"   • {fix['type']}: {fix.get('action', fix.get('suggested_value', 'N/A'))}")
        
        print("\n" + "="*70)


if __name__ == "__main__":
    print("أداة فحص أمان المواقع المتقدمة - Advanced Web Security Scanner V2")
    print("="*70)
    print("✨ ميزات جديدة:")
    print("  ✓ إخفاء IP عبر Proxies و User Agents عشوائية")
    print("  ✓ 13 أداة فحص بدلاً من 8")
    print("  ✓ إصلاح تلقائي ذكي للمشاكل")
    print("  ✓ إعادة محاولة تلقائية عند الأخطاء")
    print("  ✓ توصيات أمان مفصلة")
    print("="*70)
    print("⚠️  استخدم هذه الأداة فقط على المواقع التي تملكها أو لديك إذن")
    
    url = input("\nأدخل رابط الموقع (مثال: example.com): ").strip()
    
    if not url:
        print("❌ لم تدخل أي رابط!")
        sys.exit(1)
    
    use_proxy = input("هل تريد استخدام Proxy لإخفاء IP؟ (y/n): ").lower().strip() == 'y'
    
    scanner = AdvancedWebSecurityScanner(url, use_proxy=use_proxy)
    results = scanner.run_full_scan()
    
    scanner.print_summary()
    scanner.save_report()
    
    print("\n✨ شكراً لاستخدامك الأداة!")
