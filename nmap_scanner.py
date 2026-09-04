#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص Nmap المتقدم - فحص المنافذ والخدمات بقوة كاملة
Nmap Advanced Scanner - Full Port & Service Discovery
يكتشف جميع المنافذ المفتوحة والخدمات والإصدارات والثغرات
"""

import subprocess
import json
import re
import os
import sys
import socket
from typing import Dict, List, Tuple
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
import threading

class NmapScanner:
    """فاحص Nmap المتقدم والشامل"""
    
    def __init__(self, target: str):
        self.target = target
        self.domain = target.replace('https://', '').replace('http://', '').split('/')[0]
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'target': self.target,
            'domain': self.domain,
            'open_ports': [],
            'closed_ports': [],
            'filtered_ports': [],
            'services': [],
            'vulnerabilities': [],
            'os_detection': None,
            'service_versions': [],
            'hidden_services': [],
            'ddos_vulnerabilities': [],
            'exploit_suggestions': []
        }
    
    def install_nmap(self):
        """تثبيت Nmap تلقائي"""
        print("🔧 تثبيت Nmap...")
        commands = [
            ['sudo', 'apt-get', 'install', '-y', 'nmap'],
            ['brew', 'install', 'nmap'],
            ['sudo', 'yum', 'install', '-y', 'nmap'],
            ['sudo', 'pacman', '-S', 'nmap']
        ]
        
        for cmd in commands:
            try:
                print(f"  محاولة: {' '.join(cmd[:3])}")
                subprocess.run(cmd, timeout=120)
                print("✅ تم تثبيت Nmap")
                return True
            except:
                continue
        
        print("❌ فشل التثبيت - يرجى التثبيت يدويًا من: https://nmap.org/download")
        return False
    
    def is_nmap_installed(self):
        """التحقق من تثبيت Nmap"""
        try:
            subprocess.run(['nmap', '--version'], capture_output=True, timeout=5)
            return True
        except:
            return False
    
    def full_port_scan(self):
        """فحص شامل لجميع المنافذ (0-65535)"""
        print("\n🔥 فحص شامل لجميع المنافذ 0-65535...")
        
        if not self.is_nmap_installed():
            self.install_nmap()
        
        ip = self._resolve_ip()
        if not ip:
            print(f"❌ لا يمكن حل النطاق {self.domain}")
            return None
        
        # الفحص الشامل
        cmd = [
            'nmap',
            '-p-',  # جميع المنافذ
            '-sS',  # TCP SYN scan (أسرع)
            '-T4',  # سرعة عالية
            '-v',   # verbose
            '--open',  # المنافذ المفتوحة فقط
            '-oX', 'nmap_full.xml',
            ip
        ]
        
        try:
            print(f"  🚀 فحص: nmap -p- -sS -T4 {ip}")
            result = subprocess.run(cmd, timeout=3600, capture_output=True, text=True)
            self._parse_nmap_xml('nmap_full.xml')
            print(f"  ✅ وجدت {len(self.results['open_ports'])} منفذ مفتوح")
        except subprocess.TimeoutExpired:
            print("  ⏱️ انتهت مهلة الفحص الشامل")
        except Exception as e:
            print(f"  ❌ خطأ: {e}")
    
    def service_version_scan(self):
        """فحص إصدارات الخدمات بدقة عالية"""
        print("\n🔍 فحص إصدارات الخدمات...")
        
        open_ports_str = ','.join([str(p['port']) for p in self.results['open_ports']])
        if not open_ports_str:
            print("  لا توجد منافذ مفتوحة للفحص")
            return
        
        ip = self._resolve_ip()
        
        cmd = [
            'nmap',
            '-p', open_ports_str,
            '-sV',  # كشف الإصدار
            '-sC',  # NSE scripts
            '--script', 'default,vuln',  # تشغيل جميع البرامج النصية
            '-O',   # كشف نظام التشغيل
            '-A',   # فحص شامل (OS, version, script, traceroute)
            '-T4',
            '-v',
            '-oX', 'nmap_services.xml',
            ip
        ]
        
        try:
            print(f"  🚀 فحص الخدمات والإصدارات...")
            subprocess.run(cmd, timeout=1800, capture_output=True, text=True)
            self._parse_service_versions('nmap_services.xml')
            print(f"  ✅ وجدت {len(self.results['service_versions'])} خدمة")
        except Exception as e:
            print(f"  ❌ خطأ: {e}")
    
    def vulnerability_scan(self):
        """فحص الثغرات الأمنية"""
        print("\n⚠️ فحص الثغرات الأمنية...")
        
        ip = self._resolve_ip()
        open_ports_str = ','.join([str(p['port']) for p in self.results['open_ports']])
        
        if not open_ports_str:
            return
        
        # استخدام NSE vuln scripts
        cmd = [
            'nmap',
            '-p', open_ports_str,
            '--script', 'vuln',
            '-sV',
            '-v',
            '-oX', 'nmap_vuln.xml',
            ip
        ]
        
        try:
            print(f"  🚀 تشغيل برامج الثغرات...")
            subprocess.run(cmd, timeout=1800, capture_output=True, text=True)
            self._parse_vulnerabilities('nmap_vuln.xml')
            print(f"  ✅ وجدت {len(self.results['vulnerabilities'])} ثغرة محتملة")
        except Exception as e:
            print(f"  ❌ خطأ: {e}")
    
    def os_detection_scan(self):
        """كشف نظام التشغيل"""
        print("\n🖥️ فحص نظام التشغيل...")
        
        ip = self._resolve_ip()
        
        cmd = [
            'nmap',
            '-O',
            '-v',
            '--osscan-guess',  # تخمين في حالة عدم التأكد
            '-oX', 'nmap_os.xml',
            ip
        ]
        
        try:
            subprocess.run(cmd, timeout=600, capture_output=True, text=True)
            self._parse_os_detection('nmap_os.xml')
            if self.results['os_detection']:
                print(f"  ✅ نظام التشغيل المكتشف: {self.results['os_detection']['os']}")
        except Exception as e:
            print(f"  ❌ خطأ: {e}")
    
    def aggressive_scan(self):
        """فحص عدواني شامل (استخدم بحذر)"""
        print("\n💥 فحص عدواني شامل...")
        
        ip = self._resolve_ip()
        
        cmd = [
            'nmap',
            '-p-',
            '-A',  # فحص شامل
            '--script', 'default,vuln,discovery',
            '-sV', '-O',
            '-T5',  # أقصى سرعة
            '--version-light',
            '-v',
            '-oX', 'nmap_aggressive.xml',
            ip
        ]
        
        try:
            print(f"  🚀 بدء الفحص العدواني (قد يستغرق وقتًا)...")
            subprocess.run(cmd, timeout=3600, capture_output=True, text=True)
            self._parse_nmap_xml('nmap_aggressive.xml')
        except Exception as e:
            print(f"  ❌ خطأ: {e}")
    
    def scan_hidden_services(self):
        """فحص الخدمات المخفية والمنافذ غير الشهيرة"""
        print("\n🔎 فحص الخدمات المخفية...")
        
        ip = self._resolve_ip()
        
        # فحص المنافذ غير الشهيرة والمشبوهة
        suspicious_ports = [
            '3128', '8008', '8888', '9000', '9999',
            '4444', '5555', '6666', '7777',
            '1337', '31337',  # backdoor ports
            '27017', '27018', '27019',  # MongoDB
            '5432', '5433',  # PostgreSQL
            '3306', '3307',  # MySQL
            '6379', '6380',  # Redis
            '11211',  # Memcached
            '50070', '50470',  # Hadoop
            '8161', '8162',  # ActiveMQ
        ]
        
        ports_str = ','.join(suspicious_ports)
        
        cmd = [
            'nmap',
            '-p', ports_str,
            '-sV',
            '-v',
            '-oX', 'nmap_hidden.xml',
            ip
        ]
        
        try:
            print(f"  🚀 فحص {len(suspicious_ports)} منفذ مشبوه...")
            subprocess.run(cmd, timeout=600, capture_output=True, text=True)
            self._parse_hidden_services('nmap_hidden.xml')
            print(f"  ✅ وجدت {len(self.results['hidden_services'])} خدمة مخفية")
        except Exception as e:
            print(f"  ❌ خطأ: {e}")
    
    def _resolve_ip(self) -> str:
        """حل النطاق إلى عنوان IP"""
        try:
            ip = socket.gethostbyname(self.domain)
            return ip
        except:
            return None
    
    def _parse_nmap_xml(self, filename):
        """تحليل ملف XML من Nmap"""
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            
            for host in root.findall('host'):
                for port in host.findall('ports/port'):
                    port_num = port.get('portid')
                    state = port.find('state').get('state')
                    service = port.find('service')
                    service_name = service.get('name') if service is not None else 'unknown'
                    
                    port_info = {
                        'port': int(port_num),
                        'state': state,
                        'service': service_name
                    }
                    
                    if state == 'open':
                        self.results['open_ports'].append(port_info)
                        print(f"  ✅ المنفذ {port_num}: مفتوح ({service_name})")
                    elif state == 'closed':
                        self.results['closed_ports'].append(port_info)
                    elif state == 'filtered':
                        self.results['filtered_ports'].append(port_info)
        except Exception as e:
            print(f"  ❌ خطأ في تحليل XML: {e}")
    
    def _parse_service_versions(self, filename):
        """تحليل إصدارات الخدمات"""
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            
            for host in root.findall('host'):
                for port in host.findall('ports/port'):
                    port_num = port.get('portid')
                    service = port.find('service')
                    
                    if service is not None:
                        service_info = {
                            'port': port_num,
                            'name': service.get('name', 'unknown'),
                            'product': service.get('product', 'unknown'),
                            'version': service.get('version', 'unknown'),
                            'extrainfo': service.get('extrainfo', '')
                        }
                        self.results['service_versions'].append(service_info)
                        print(f"  ℹ️ المنفذ {port_num}: {service_info['product']} {service_info['version']}")
        except Exception as e:
            print(f"  ❌ خطأ في تحليل الخدمات: {e}")
    
    def _parse_vulnerabilities(self, filename):
        """تحليل الثغرات المكتشفة"""
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            
            for script in root.findall('.//script'):
                script_id = script.get('id')
                output = script.get('output', '')
                
                if output and script_id:
                    vuln = {
                        'script': script_id,
                        'details': output,
                        'severity': self._estimate_severity(script_id, output)
                    }
                    self.results['vulnerabilities'].append(vuln)
                    print(f"  ⚠️ ثغرة: {script_id}")
        except Exception as e:
            print(f"  ❌ خطأ في تحليل الثغرات: {e}")
    
    def _parse_hidden_services(self, filename):
        """تحليل الخدمات المخفية"""
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            
            for host in root.findall('host'):
                for port in host.findall('ports/port'):
                    port_num = port.get('portid')
                    state = port.find('state').get('state')
                    service = port.find('service')
                    
                    if state == 'open' and service is not None:
                        self.results['hidden_services'].append({
                            'port': port_num,
                            'service': service.get('name', 'unknown'),
                            'version': service.get('version', 'unknown')
                        })
        except Exception as e:
            print(f"  ❌ خطأ: {e}")
    
    def _parse_os_detection(self, filename):
        """تحليل كشف نظام التشغيل"""
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            
            for host in root.findall('host'):
                for osmatch in host.findall('os/osmatch'):
                    self.results['os_detection'] = {
                        'os': osmatch.get('name'),
                        'accuracy': osmatch.get('accuracy')
                    }
        except Exception as e:
            print(f"  ❌ خطأ: {e}")
    
    def _estimate_severity(self, script_id: str, output: str) -> str:
        """تقدير شدة الثغرة"""
        critical_keywords = ['critical', 'rce', 'remote code execution', 'exploit', 'vulnerability']
        high_keywords = ['high', 'buffer overflow', 'sql injection', 'xss']
        
        lower_output = output.lower()
        
        for keyword in critical_keywords:
            if keyword in lower_output:
                return 'CRITICAL'
        
        for keyword in high_keywords:
            if keyword in lower_output:
                return 'HIGH'
        
        return 'MEDIUM'
    
    def generate_comprehensive_report(self):
        """إنشاء تقرير شامل"""
        report = {
            'title': 'تقرير فحص Nmap الشامل',
            'timestamp': datetime.now().isoformat(),
            'target': self.target,
            'domain': self.domain,
            'summary': {
                'open_ports': len(self.results['open_ports']),
                'closed_ports': len(self.results['closed_ports']),
                'filtered_ports': len(self.results['filtered_ports']),
                'services': len(self.results['service_versions']),
                'vulnerabilities': len(self.results['vulnerabilities']),
                'hidden_services': len(self.results['hidden_services'])
            },
            'details': self.results
        }
        
        # حفظ التقرير
        with open('nmap_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("\n✅ تم حفظ التقرير في: nmap_report.json")
        return report
