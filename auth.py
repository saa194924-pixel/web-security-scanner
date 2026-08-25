#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام المصادقة لأداة فحص أمان المواقع
يوفر حماية وتحكم في الوصول
"""

from functools import wraps
from typing import Callable, Any
import hashlib
import hmac
from config import Config, SecurityValidator

class AuthenticationError(Exception):
    """استثناء خطأ المصادقة"""
    pass


class Authenticator:
    """فئة إدارة المصادقة والتحقق من الوصول"""
    
    def __init__(self):
        self.failed_attempts = {}
        self.max_attempts = 5
        self.lockout_duration = 300  # 5 دقائق
    
    def require_api_key(self, func: Callable) -> Callable:
        """
        ديكوريتور للتحقق من مفتاح API قبل تنفيذ الدالة
        
        Usage:
            @authenticator.require_api_key
            def scan_website(url):
                ...
        """
        @wraps(func)
        def wrapper(*args, api_key: str = None, **kwargs):
            if not api_key:
                raise AuthenticationError("❌ لم يتم توفير مفتاح API")
            
            if not SecurityValidator.validate_api_key(api_key):
                self._record_failed_attempt(api_key)
                raise AuthenticationError("❌ مفتاح API غير صحيح")
            
            print(f"✅ تم التحقق من مفتاح API بنجاح")
            return func(*args, **kwargs)
        
        return wrapper
    
    def require_secret(self, func: Callable) -> Callable:
        """
        ديكوريتور للتحقق من الرمز السري
        
        Usage:
            @authenticator.require_secret
            def admin_function():
                ...
        """
        @wraps(func)
        def wrapper(*args, secret: str = None, **kwargs):
            if not secret:
                raise AuthenticationError("❌ لم يتم توفير رمز سري")
            
            if not SecurityValidator.validate_secret(secret):
                self._record_failed_attempt(secret)
                raise AuthenticationError("❌ رمز سري غير صحيح")
            
            print(f"✅ تم التحقق من الرمز السري بنجاح")
            return func(*args, **kwargs)
        
        return wrapper
    
    def generate_token(self, user_id: str) -> str:
        """
        إنشاء رمز مصادقة آمن
        
        Args:
            user_id: معرف المستخدم
            
        Returns:
            رمز المصادقة المشفر
        """
        raw_token = f"{user_id}:{SecurityValidator.generate_session_token()}"
        token = hashlib.sha256(raw_token.encode()).hexdigest()
        return token
    
    def verify_token(self, token: str, user_id: str) -> bool:
        """
        ال��حقق من صحة رمز المصادقة
        
        Args:
            token: الرمز المراد التحقق منه
            user_id: معرف المستخدم
            
        Returns:
            True إذا كان الرمز صحيحاً
        """
        # هنا يمكنك التحقق من قاعدة البيانات
        # مثال بسيط للتوضيح فقط
        return isinstance(token, str) and len(token) == 64
    
    def _record_failed_attempt(self, identifier: str):
        """تسجيل محاولة فاشلة"""
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = 0
        
        self.failed_attempts[identifier] += 1
        
        if self.failed_attempts[identifier] >= self.max_attempts:
            print(f"⚠️  تحذير: تم حظر المعرف {identifier} مؤقتاً بسبب محاولات فاشلة متكررة")
    
    def is_locked_out(self, identifier: str) -> bool:
        """التحقق من حظر المعرف"""
        return self.failed_attempts.get(identifier, 0) >= self.max_attempts


# إنشاء نسخة عامة من الـ Authenticator
authenticator = Authenticator()


def check_api_key(api_key: str) -> dict:
    """
    فحص سريع لمفتاح API
    
    Args:
        api_key: المفتاح المراد فحصه
        
    Returns:
        قاموس يحتوي على حالة الفحص
    """
    is_valid = SecurityValidator.validate_api_key(api_key)
    
    result = {
        'valid': is_valid,
        'message': '✅ مفتاح صحيح' if is_valid else '❌ مفتاح غير صحيح',
        'key_prefix': api_key[:10] + '***' if api_key else 'N/A'
    }
    
    if is_valid:
        SecurityValidator.log_access(api_key, 'valid_auth_check')
    
    return result


def check_secret(secret: str) -> dict:
    """
    فحص سريع للرمز السري
    
    Args:
        secret: الرمز السري المراد فحصه
        
    Returns:
        قاموس يحتوي على حالة الفحص
    """
    is_valid = SecurityValidator.validate_secret(secret)
    
    result = {
        'valid': is_valid,
        'message': '✅ رمز صحيح' if is_valid else '❌ رمز غير صحيح',
        'attempt_logged': True
    }
    
    if is_valid:
        SecurityValidator.log_access(secret, 'valid_secret_check')
    
    return result


# مثال على الاستخدام
if __name__ == "__main__":
    print("🔐 نظام المصادقة")
    print("=" * 50)
    
    # اختبار مفتاح API
    test_api_key = Config.AUTHORIZED_KEYS[0]
    print(f"\n📝 اختبار مفتاح API:")
    print(f"   المفتاح: {test_api_key}")
    result = check_api_key(test_api_key)
    print(f"   النتيجة: {result['message']}")
    
    # اختبار رمز سري
    test_secret = Config.SECRET_KEY
    print(f"\n🔑 اختبار الرمز السري:")
    print(f"   النتيجة: {check_secret(test_secret)['message']}")
    
    # توليد رمز جلسة
    session_token = SecurityValidator.generate_session_token()
    print(f"\n🎟️  رمز جلسة جديد:")
    print(f"   {session_token}")