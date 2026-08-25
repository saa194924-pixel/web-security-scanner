#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعدادات أداة فحص أمان المواقع
تضمن المفاتيح السرية والتكوينات
"""

import os
import secrets
from datetime import datetime

# ============ مفاتيح سرية ============
class Config:
    """فئة التكوين الرئيسية"""
    
    # رمز سري لأداة الفحص
    SECRET_KEY = os.environ.get('SCANNER_SECRET', 'iraq2003-web-scanner-secret-key')
    
    # مفتاح API للمصادقة
    API_KEY = os.environ.get('SCANNER_API_KEY', secrets.token_urlsafe(32))
    
    # قائمة المفاتيح المصرح بها
    AUTHORIZED_KEYS = [
        API_KEY,
        'sk_live_premium_scanner_2026',
        'admin_access_token_secure'
    ]
    
    # إعدادات الفحص
    DEFAULT_TIMEOUT = 5
    MAX_RETRIES = 3
    SCAN_RATE_LIMIT = 10  # عدد الفحوصات في الدقيقة
    
    # الملفات المحظورة من الحذف
    PROTECTED_FILES = ['.git', '.env', 'config.php', 'database.sql']
    
    # مستويات الخطورة
    SEVERITY_LEVELS = {
        'Critical': 1,      # حرجة
        'High': 2,         # عالية
        'Medium': 3,       # متوسطة
        'Low': 4           # منخفضة
    }


class SecurityValidator:
    """فئة للتحقق من الأمان والمفاتيح"""
    
    @staticmethod
    def validate_api_key(key: str) -> bool:
        """
        التحقق من صحة مفتاح API
        
        Args:
            key: المفتاح المراد التحقق منه
            
        Returns:
            True إذا كان المفتاح صحيحاً، False خلاف ذلك
        """
        if not key:
            return False
        
        return key in Config.AUTHORIZED_KEYS
    
    @staticmethod
    def validate_secret(secret: str) -> bool:
        """
        التحقق من صحة الرمز السري
        
        Args:
            secret: الرمز السري المراد التحقق منه
            
        Returns:
            True إذا كان الرمز صحيحاً
        """
        return secret == Config.SECRET_KEY
    
    @staticmethod
    def generate_session_token() -> str:
        """
        إنشاء رمز جلسة عشوائي آمن
        
        Returns:
            رمز جلسة فريد وآمن
        """
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def log_access(key: str, action: str, timestamp=None):
        """
        تسجيل محاولات الوصول
        
        Args:
            key: المفتاح المستخدم
            action: الإجراء المنفذ
            timestamp: الوقت (اختياري)
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        log_entry = f"[{timestamp}] مفتاح: {key[:10]}*** | إجراء: {action}\n"
        
        # كتابة في ملف السجل
        with open('scanner_access.log', 'a', encoding='utf-8') as f:
            f.write(log_entry)


# ============ متغيرات البيئة الآمنة ============
ENVIRONMENT_VARS = {
    'SCANNER_SECRET': 'المفتاح السري الرئيسي',
    'SCANNER_API_KEY': 'مفتاح API للمصادقة',
    'SCANNER_DEBUG': 'تفعيل نمط التصحيح',
    'SCANNER_LOG_LEVEL': 'مستوى التسجيل (DEBUG, INFO, WARNING, ERROR)'
}

print("""
⚠️  تذكير أمان مهم:
==================
1. غير المفاتيح السرية قبل النشر في الإنتاج
2. لا تضع المفاتيح في الكود مباشرة - استخدم متغيرات البيئة
3. احفظ المفاتيح في ملف .env وأضفه إلى .gitignore
4. استخدم مفاتيح قوية وعشوائية
5. دوّر المفاتيح بشكل دوري

متغيرات البيئة المطلوبة:
- SCANNER_SECRET: رمز سري قوي (32+ حرف)
- SCANNER_API_KEY: مفتاح API فريد
""")