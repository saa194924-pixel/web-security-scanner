#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة فحص أمان المواقع - Web Security Scanner
====================================
أداة شاملة لفحص أمان المواقع والكشف عن الثغرات الشهيرة
"""

import socket
import ssl
import requests
from urllib.parse import urljoin, parse_qs, urlparse
import json
from datetime import datetime
from typing import Dict, List
import re

class WebSecurityScanner:
    """فئة رئيسية لفحص أمان المواقع"""
    
    def __init__(self, url: str):
        self.url = url if url.startswith(('http://', 'https://')) else f'https://{url}'
        self.domain = urlparse(self.url).netloc
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'url': self.url,
            'vulnerabilities': [],
            'security_headers': {},
            'port_scan': {},
            'ssl_info': {}
        }
    
    # ============ 1️⃣ فحص المنافذ المفتوحة ============
    def scan_ports(self, ports: List[int] = None) -> Dict:
        """
        فحص المنافذ المفتوحة
        المنافذ الشهيرة: 80(HTTP), 443(HTTPS), 22(SSH), 21(FTP), 3306(MySQL)
        """
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 3306, 5432, 8080, 8443]
        
        print("\n🔍 جاري فحص المنافذ المفتوحة...")
        open_ports = {}
        
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            try:
                result = sock.connect_ex((self.domain, port))
                if result == 0:
                    open_ports[port] = self._get_service_name(port)
                    print(f"  ✓ المنفذ {port}: مفتوح ({self._get_service_name(port)})")
            except:
                pass
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
            5432: 'PostgreSQL', 8080: 'HTTP Alt', 8443: 'HTTPS Alt'
        }
        return services.get(port, 'Unknown')
    
    # ============ 2️⃣ فحص رؤوس الأمان ============
    def check_security_headers(self) -> Dict:
        """
        فحص رؤوس الأمان المهمة
        رؤوس الأمان تحمي من: XSS, Clickjacking, MIME sniffing
        """
        print("\n🛡️  جاري فحص رؤوس الأمان...")
        
        important_headers = {
            'Content-Security-Policy': 'منع هجمات XSS',
            'X-Content-Type-Options': 'منع MIME sniffing',
            'X-Frame-Options': 'منع Clickjacking',
            'Strict-Transport-Security': 'إجبار HTTPS',
            'X-XSS-Protection': 'حماية XSS',
            'Referrer-Policy': 'التحكم في المراجع',
            'Permissions-Policy': 'التحكم في الأذونات'
        }
        
        try:
            response = requests.get(self.url, timeout=5, verify=False)
            headers = response.headers
            
            for header, description in important_headers.items():
                if header in headers:
                    print(f"  ✓ {header}: موجود")
                    self.results['security_headers'][header] = headers[header]
                else:
                    print(f"  ✗ {header}: غير موجود - {description}")
                    self.results['vulnerabilities'].append({
                        'type': 'Missing Security Header',
                        'header': header,
                        'severity': 'Medium',
                        'description': f'رأس الأمان {header} غير موجود'
                    })
        except Exception as e:
            print(f"  ❌ خطأ في الفحص: {str(e)}")
        
        return self.results['security_headers']
    
    # ============ 3️⃣ فحص SSL/TLS ============
    def check_ssl(self) -> Dict:
        """
        فحص شهادة SSL/TLS
        تحقق من: صلاحية الشهادة، التشفير، البروتوكول
        """
        print("\n🔐 جاري فحص SSL/TLS...")
        
        try:
            hostname = self.domain
            port = 443
            
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    protocol = ssock.version()
                    
                    self.results['ssl_info'] = {
                        'protocol': protocol,
                        'cipher': cipher[0],
                        'certificate_subject': cert['subject'],
                        'issuer': cert['issuer'],
                        'valid_from': cert['notBefore'],
                        'valid_until': cert['notAfter']
                    }
                    
                    print(f"  ✓ البروتوكول: {protocol}")
                    print(f"  ✓ Cipher: {cipher[0]}")
                    print(f"  ✓ الصلاحية: {cert['notAfter']}")
                    
                    # تحذير من بروتوكولات قديمة
                    if protocol in ['SSLv2', 'SSLv3', 'TLSv1.0', 'TLSv1.1']:
                        self.results['vulnerabilities'].append({
                            'type': 'Outdated SSL/TLS Protocol',
                            'protocol': protocol,
                            'severity': 'High',
                            'description': f'البروتوكول {protocol} قديم وغير آمن'
                        })
                        print(f"  ⚠️  تحذير: البروتوكول {protocol} قديم!")
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
        
        return self.results['ssl_info']
    
    # ============ 4️⃣ فحص ثغرات XSS ============
    def check_xss(self) -> List:
        """
        فحص ثغرات Cross-Site Scripting (XSS)
        XSS: حقن كود JavaScript في الصفحة
        """
        print("\n⚠️  جاري فحص ثغرات XSS...")
        
        xss_payloads = [
            '<script>alert("XSS")</script>',
            '"><script>alert("XSS")</script>',
            'javascript:alert("XSS")',
            '<img src=x onerror="alert(\'XSS\')">'
        ]
        
        try:
            for param in ['q', 'search', 'id', 'name', 'input']:
                test_url = f'{self.url}?{param}=test'
                response = requests.get(test_url, timeout=5, verify=False)
                
                if 'test' in response.text and response.status_code == 200:
                    print(f"  ⚠️  المعامل '{param}' قد يكون عرضة لـ XSS")
                    self.results['vulnerabilities'].append({
                        'type': 'Potential XSS',
                        'parameter': param,
                        'severity': 'High',
                        'description': f'المعامل {param} قد لا يتم تصفيته بشكل صحيح'
                    })
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
        
        return self.results['vulnerabilities']
    
    # ============ 5️⃣ فحص SQL Injection ============
    def check_sql_injection(self) -> List:
        """
        فحص ثغرات SQL Injection
        SQL Injection: حقن أكواد SQL غير مصرحة
        """
        print("\n⚠️  جاري فحص ثغرات SQL Injection...")
        
        sql_payloads = ["' OR '1'='1", "1' OR '1'='1", "admin'--", "' OR 1=1--"]
        
        try:
            for param in ['id', 'user', 'username', 'password', 'email']:
                for payload in sql_payloads:
                    test_url = f'{self.url}?{param}={payload}'
                    try:
                        response = requests.get(test_url, timeout=3, verify=False)
                        # علامات تدل على SQL Injection
                        if any(indicator in response.text.lower() for indicator in 
                               ['sql', 'syntax', 'mysql', 'error', 'exception']):
                            self.results['vulnerabilities'].append({
                                'type': 'Potential SQL Injection',
                                'parameter': param,
                                'payload': payload,
                                'severity': 'Critical',
                                'description': f'المعامل {param} قد يكون عرضة لـ SQL Injection'
                            })
                            print(f"  🔴 خطر! المعامل '{param}' قد يكون عرضة لـ SQL Injection")
                    except:
                        pass
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
        
        return self.results['vulnerabilities']
    
    # ============ 6️⃣ فحص CSRF Tokens ============
    def check_csrf_protection(self) -> Dict:
        """
        فحص حماية CSRF
        CSRF: جعل المستخدم ينفذ عملية بدون إرادته
        """
        print("\n🔍 جاري فحص حماية CSRF...")
        
        csrf_token_names = ['csrf_token', '_csrf', 'authenticity_token', 'token', '_token']
        
        try:
            response = requests.get(self.url, timeout=5, verify=False)
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
                    'description': 'قد لا توجد حماية كافية من هجمات CSRF'
                })
            
            return {'csrf_tokens_found': found_tokens}
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
            return {}
    
    # ============ 7️⃣ فحص التكوين الخاطئ ============
    def check_misconfigurations(self) -> List:
        """
        فحص أخطاء التكوين الشهيرة
        مثل: ملفات مرفوعة، ملفات احتياطية، ملفات config
        """
        print("\n🔧 جاري فحص أخطاء التكوين...")
        
        suspicious_paths = [
            '/.git/', '/.env', '/config.php', '/web.config',
            '/backup/', '/admin/', '/test/', '/debug.log',
            '/database.sql', '/.htaccess', '/robots.txt',
            '/sitemap.xml', '/xmlrpc.php', '/wp-admin/'
        ]
        
        for path in suspicious_paths:
            test_url = urljoin(self.url, path)
            try:
                response = requests.head(test_url, timeout=3, verify=False)
                if response.status_code in [200, 301, 302]:
                    print(f"  ⚠️  وجدنا: {path} (Status: {response.status_code})")
                    self.results['vulnerabilities'].append({
                        'type': 'Information Disclosure',
                        'path': path,
                        'status_code': response.status_code,
                        'severity': 'Medium',
                        'description': f'المسار {path} متاح وقد يسرب معلومات'
                    })
            except:
                pass
        
        return self.results['vulnerabilities']
    
    # ============ 8️⃣ فحص Server Info ============
    def check_server_info(self) -> Dict:
        """
        الحصول على معلومات الخادم
        معرفة نوع الخادم والإصدار تساعد في اختيار الهجمات المناسبة
        """
        print("\n📊 جاري جمع معلومات الخادم...")
        
        try:
            response = requests.get(self.url, timeout=5, verify=False)
            headers = response.headers
            
            server_info = {
                'Server': headers.get('Server', 'Unknown'),
                'X-Powered-By': headers.get('X-Powered-By', 'Unknown'),
                'Content-Type': headers.get('Content-Type', 'Unknown'),
                'Status-Code': response.status_code
            }
            
            for key, value in server_info.items():
                if value != 'Unknown':
                    print(f"  ℹ️  {key}: {value}")
            
            return server_info
        except Exception as e:
            print(f"  ❌ خطأ: {str(e)}")
            return {}
    
    # ============ تشغيل الفحص الكامل ============
    def run_full_scan(self) -> Dict:
        """تشغيل جميع الفحوصات"""
        print("\n" + "="*60)
        print("🚀 بدء فحص أمان الموقع الشامل")
        print(f"   الموقع: {self.url}")
        print("="*60)
        
        self.scan_ports()
        self.check_security_headers()
        self.check_ssl()
        self.check_server_info()
        self.check_csrf_protection()
        self.check_xss()
        self.check_sql_injection()
        self.check_misconfigurations()
        
        return self.results
    
    # ============ حفظ التقرير ============
    def save_report(self, filename: str = None) -> str:
        """حفظ التقرير في ملف JSON"""
        if filename is None:
            filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ تم حفظ التقرير في: {filename}")
        return filename
    
    # ============ طباعة ملخص النتائج ============
    def print_summary(self):
        """طباعة ملخص الثغرات المكتشفة"""
        print("\n" + "="*60)
        print("📋 ملخص النتائج")
        print("="*60)
        
        vulns = self.results['vulnerabilities']
        
        if not vulns:
            print("\n✅ لم يتم اكتشاف ثغرات!")
        else:
            print(f"\n⚠️  تم اكتشاف {len(vulns)} ثغرة:")
            
            # تصنيف حسب الخطورة
            critical = [v for v in vulns if v.get('severity') == 'Critical']
            high = [v for v in vulns if v.get('severity') == 'High']
            medium = [v for v in vulns if v.get('severity') == 'Medium']
            
            if critical:
                print(f"\n🔴 حرجة ({len(critical)}):")
                for v in critical:
                    print(f"   - {v['type']}: {v['description']}")
            
            if high:
                print(f"\n🟠 عالية ({len(high)}):")
                for v in high:
                    print(f"   - {v['type']}: {v['description']}")
            
            if medium:
                print(f"\n🟡 متوسطة ({len(medium)}):")
                for v in medium:
                    print(f"   - {v['type']}: {v['description']}")
        
        print("\n" + "="*60)


if __name__ == "__main__":
    print("أداة فحص أمان المواقع - Web Security Scanner")
    print("⚠️  استخدم هذه الأداة فقط على المواقع التي تملكها أو لديك إذن")
    
    url = input("\nأدخل رابط الموقع (مثال: example.com): ").strip()
    
    if not url:
        print("❌ لم تدخل أي رابط!")
        exit(1)
    
    scanner = WebSecurityScanner(url)
    results = scanner.run_full_scan()
    
    scanner.print_summary()
    scanner.save_report()
