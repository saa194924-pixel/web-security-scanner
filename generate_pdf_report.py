#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تقرير PDF شامل - أداة فحص أمان المواقع المتقدمة
Advanced Web Security Scanner V2 - Comprehensive PDF Report
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

# تسجيل الخطوط العربية
try:
    pdfmetrics.registerFont(TTFont('Arabic', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('ArabicBold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
except:
    print("⚠️ تحذير: لم يتم تحميل الخطوط العربية بنجاح")
    pdfmetrics.registerFont(TTFont('Arabic', 'Arial'))
    pdfmetrics.registerFont(TTFont('ArabicBold', 'Arial'))

def create_security_scanner_report(filename='Security_Scanner_Report.pdf'):
    """إنشاء تقرير PDF شامل عن أداة فحص الأمان"""
    
    # إنشاء المستند
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        title="تقرير أداة فحص أمان المواقع",
        author="Advanced Web Security Scanner"
    )
    
    # قائمة العناصر
    elements = []
    
    # الأنماط
    styles = getSampleStyleSheet()
    
    # نمط مخصص للعناوين الرئيسية
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='ArabicBold',
        bold=True
    )
    
    # نمط للعناوين الفرعية
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#283593'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='ArabicBold',
        bold=True,
        borderColor=colors.HexColor('#1a237e'),
        borderWidth=2,
        borderPadding=10,
        backColor=colors.HexColor('#f5f5f5')
    )
    
    # نمط النص العادي
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_RIGHT,
        fontName='Arabic',
        spaceAfter=6,
        leading=18
    )
    
    # ========== الصفحة الأولى ==========
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("أداة فحص أمان المواقع المتقدمة", title_style))
    elements.append(Paragraph("Advanced Web Security Scanner V2", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # معلومات التقرير
    info_data = [
        ['تاريخ التقرير:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['الإصدار:', 'Version 2.0'],
        ['اللغة:', 'العربية / English'],
        ['النوع:', 'تقرير شامل'],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (0, -1), 'ArabicBold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # الملخص التنفيذي
    elements.append(Paragraph("📋 الملخص التنفيذي", heading_style))
    elements.append(Paragraph(
        "أداة فحص أمان المواقع المتقدمة (Advanced Web Security Scanner V2) هي أداة احترافية شاملة "
        "مصممة لفحص أمان تطبيقات الويب والكشف عن الثغرات الأمنية. توفر الأداة 13 فحص أمان متقدم "
        "مع إمكانيات إخفاء IP والإصلاح التلقائي والتقارير التفصيلية.",
        normal_style
    ))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(PageBreak())
    
    # ========== الميزات الرئيسية ==========
    elements.append(Paragraph("✨ الميزات الرئيسية", heading_style))
    
    features_data = [
        ['الميزة', 'الوصف'],
        ['13 أداة فحص متقدمة', 'فحوصات شاملة لجميع جوانب الأمان'],
        ['إخفاء IP', 'استخدام Proxies و User Agents عشوائية'],
        ['إصلاح تلقائي ذكي', 'اقتراحات وإصلاحات تلقائية للمشاكل'],
        ['إعادة محاولة تلقائية', 'معالجة أخطاء متقدمة مع Exponential Backoff'],
        ['توصيات أمان مفصلة', 'حلول واضحة لكل ثغرة'],
        ['تقارير JSON', 'تقارير منظمة وسهلة التحليل'],
        ['مقاييس الأداء', 'إحصائيات شاملة عن الفحص'],
        ['واجهة عربية كاملة', 'دعم كامل للغة العربية'],
    ]
    
    features_table = Table(features_data, colWidths=[2*inch, 3.5*inch])
    features_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'ArabicBold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#e8eaf6')]),
    ]))
    elements.append(features_table)
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(PageBreak())
    
    # ========== الفحوصات ال 13 ==========
    elements.append(Paragraph("🔍 شرح تفصيلي للفحوصات الـ 13", heading_style))
    
    checks = [
        {
            'num': '1️⃣',
            'name': 'فحص المنافذ المفتوحة',
            'en_name': 'Port Scanning',
            'desc': 'اكتشاف المنافذ المفتوحة على الخادم ومعرفة الخدمات المشغلة عليها (FTP, SSH, MySQL, إلخ)',
            'threat': 'خطر عالي - منافذ مفتوحة تعني خدمات قد تحتوي على ثغرات',
            'solution': 'إغلاق المنافذ غير الضرورية وتفعيل جدران النار'
        },
        {
            'num': '2️⃣',
            'name': 'فحص رؤوس الأمان',
            'en_name': 'Security Headers',
            'desc': 'التحقق من وجود رؤوس حماية مهمة مثل CSP و X-Frame-Options و HSTS',
            'threat': 'خطر متوسط - عدم وجود رؤوس الأمان يز��د من خطر الهجمات',
            'solution': 'إضافة جميع رؤوس الأمان الموصى بها في خادم الويب'
        },
        {
            'num': '3️⃣',
            'name': 'فحص SSL/TLS',
            'en_name': 'SSL/TLS Check',
            'desc': 'التحقق من شهادات التشفير والبروتوكولات المستخدمة وقوة التشفير',
            'threat': 'خطر عالي جداً - بروتوكولات قديمة معرضة للاختراق',
            'solution': 'استخدام TLS 1.2 أو الأحدث وتحديث الشهادات'
        },
        {
            'num': '4️⃣',
            'name': 'فحص XSS',
            'en_name': 'Cross-Site Scripting (XSS)',
            'desc': 'البحث عن ثغرات حقن أكواد JavaScript التي قد تسرق بيانات المستخدمين',
            'threat': 'خطر عالي جداً - يمكن سرقة كلمات المرور والجلسات',
            'solution': 'تطبيق HTML Entity Encoding وفلترة جميع المدخلات'
        },
        {
            'num': '5️⃣',
            'name': 'فحص SQL Injection',
            'en_name': 'SQL Injection',
            'desc': 'البحث عن ثغرات حقن أوامر SQL التي تس��ح بالوصول لقاعدة البيانات',
            'threat': 'خطر حرج جداً - يمكن سرقة جميع البيانات وحذفها',
            'solution': 'استخدام Prepared Statements و Parameterized Queries'
        },
        {
            'num': '6️⃣',
            'name': 'فحص CSRF',
            'en_name': 'Cross-Site Request Forgery',
            'desc': 'التحقق من وجود حماية ضد الطلبات المزيفة التي تجعل المستخدم ينفذ عمليات بدون إرادته',
            'threat': 'خطر عالي - يمكن تحويل أموال أو تغيير بيانات',
            'solution': 'إضافة CSRF tokens والتحقق منها على كل طلب POST'
        },
        {
            'num': '7️⃣',
            'name': 'فحص التكوين الخاطئ',
            'en_name': 'Misconfiguration Detection',
            'desc': 'البحث عن ملفات وملجدات حساسة معرضة مثل .env و .git و /backup',
            'threat': 'خطر عالي - قد تسرب كلمات مرور و API keys',
            'solution': 'إخفاء الملفات الحساسة وتقييد الوصول إليها'
        },
        {
            'num': '8️⃣',
            'name': 'معلومات الخادم',
            'en_name': 'Server Information',
            'desc': 'جمع بيانات عن نوع الخادم والإصدار والتكنولوجيا المستخدمة',
            'threat': 'خطر متوسط - معرفة الإصدارات القديمة تساعد الهاكرز',
            'solution': 'تحديث الخادم والبرامج وإخفاء رقم الإصدار'
        },
        {
            'num': '9️⃣',
            'name': 'فحص أمان Cookies',
            'en_name': 'Cookie Security',
            'desc': 'التحقق من أن Cookies محمية بـ flags Secure و HttpOnly و SameSite',
            'threat': 'خطر عالي - Cookies غير آمنة قد تسرق جلسات المستخدمين',
            'solution': 'إضافة جميع flags الأمان للـ Cookies'
        },
        {
            'num': '🔟',
            'name': 'إجبار HTTPS',
            'en_name': 'HTTPS Enforcement',
            'desc': 'التحقق من أن الموقع يفرض استخدام HTTPS ولا يسمح بـ HTTP',
            'threat': 'خطر عالي - HTTP غير مشفر والبيانات قد تُختطف',
            'solution': 'تفعيل HSTS وإعادة توجيه HTTP 301 إلى HTTPS'
        },
        {
            'num': '1️⃣1️⃣',
            'name': 'Rate Limiting',
            'en_name': 'Rate Limiting Protection',
            'desc': 'التحقق من وجود حماية ضد الهجمات الآلية والقوة الغاشمة',
            'threat': 'خطر متوسط - بدون Rate Limiting يمكن تخمين كلمات المرور',
            'solution': 'تحديد عدد الطلبات المسموحة والحظر بعدها'
        },
        {
            'num': '1️⃣2️⃣',
            'name': 'الحقول المخفية',
            'en_name': 'Hidden Fields Detection',
            'desc': 'اكتشاف حقول مخفية قد تحتوي على بيانات حساسة قابلة للتعديل',
            'threat': 'خطر متوسط - المستخدم قد يعدل الحقول المخفية',
            'solution': 'التحقق من صحة البيانات على الخادم دائماً'
        },
        {
            'num': '1️⃣3️⃣',
            'name': 'حماية Bot',
            'en_name': 'Bot Protection',
            'desc': 'التحقق من وجود CAPTCHA أو حماية ضد الروبوتات الآلية',
            'threat': 'خطر منخفض إلى متوسط - الهجمات الآلية قد تعطل الخدمة',
            'solution': 'إضافة reCAPTCHA أو حماية Cloudflare'
        },
    ]
    
    for i, check in enumerate(checks):
        elements.append(Paragraph(
            f"{check['num']} {check['name']} ({check['en_name']})",
            ParagraphStyle(
                'CheckTitle',
                parent=styles['Heading3'],
                fontSize=12,
                textColor=colors.HexColor('#1a237e'),
                spaceAfter=6,
                spaceBefore=6,
                fontName='ArabicBold',
                bold=True
            )
        ))
        
        check_content = f"""
        <b>الوصف:</b> {check['desc']}<br/>
        <b>⚠️ التهديد:</b> {check['threat']}<br/>
        <b>✅ الحل:</b> {check['solution']}
        """
        
        elements.append(Paragraph(check_content, normal_style))
        elements.append(Spacer(1, 0.15*inch))
        
        if (i + 1) % 3 == 0 and i < len(checks) - 1:
            elements.append(PageBreak())
    
    elements.append(PageBreak())
    
    # ========== كيفية الاستخدام ==========
    elements.append(Paragraph("🚀 كيفية الاستخدام", heading_style))
    
    usage_steps = [
        "تشغيل الأداة: python3 scanner_v2.py",
        "إدخال رابط الموقع المراد فحصه (مثال: example.com)",
        "اختيار استخدام Proxy لإخفاء IP (اختياري)",
        "انتظار انتهاء الفحص الشامل",
        "مراجعة النتائج والثغرات المكتشفة",
        "تطبيق التوصيات والإصلاحات",
        "حفظ التقرير بصيغة JSON",
    ]
    
    usage_data = [[f"{i+1}. {step}"] for i, step in enumerate(usage_steps)]
    
    usage_table = Table(usage_data, colWidths=[5.5*inch])
    usage_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Arabic'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#e8eaf6')]),
    ]))
    elements.append(usage_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ========== متطلبات التثبيت ==========
    elements.append(Paragraph("📦 متطلبات التثبيت", heading_style))
    
    requirements_text = """
    <b>المكتبات المطلوبة:</b><br/>
    • Python 3.7 أو أحدث<br/>
    • requests - لإرسال الطلبات HTTP<br/>
    • socket - لفحص المنافذ<br/>
    • ssl - للتعامل مع شهادات SSL/TLS<br/>
    • json - لحفظ التقارير<br/>
    • re - للتعبيرات النمطية<br/>
    <br/>
    <b>التثبيت:</b><br/>
    pip install requests<br/>
    <br/>
    <b>التشغيل:</b><br/>
    python3 scanner_v2.py
    """
    
    elements.append(Paragraph(requirements_text, normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(PageBreak())
    
    # ========== مستويات الخطورة ==========
    elements.append(Paragraph("🎯 مستويات الخطورة", heading_style))
    
    severity_data = [
        ['المستوى', 'اللون', 'الوصف', 'الإجراء'],
        ['🔴 حرج (Critical)', 'أحمر', 'ثغرة قد تسبب اختراق كامل للموقع', 'إصلاح فوري'],
        ['🟠 عالي (High)', 'برتقالي', 'ثغرة خطيرة قد تسبب فقدان بيانات', 'إصلاح سريع'],
        ['🟡 متوسط (Medium)', 'أصفر', 'ثغرة تحتاج إلى انتباه', 'إصلاح قريب'],
        ['🟢 منخفض (Low)', 'أخضر', 'ثغرة بسيطة', 'إصلاح عند التحديث التالي'],
    ]
    
    severity_table = Table(severity_data, colWidths=[1.3*inch, 1*inch, 2*inch, 1.3*inch])
    severity_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'ArabicBold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#ffebee')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#fff3e0')),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#fffde7')),
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#e8f5e9')),
    ]))
    elements.append(severity_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ========== أمثلة على الثغرات ==========
    elements.append(Paragraph("💥 أمثلة على الثغرات الشهيرة", heading_style))
    
    vulnerabilities_text = """
    <b>1. SQL Injection:</b><br/>
    المهاجم يدخل: ' OR '1'='1<br/>
    النتيجة: الوصول لجميع بيانات قاعدة البيانات دون التحقق من الهوية<br/>
    <br/>
    <b>2. XSS (Cross-Site Scripting):</b><br/>
    المهاجم يدخل: &lt;script&gt;stealCookie()&lt;/script&gt;<br/>
    النتيجة: سرقة جلسات المستخدمين وبياناتهم الحساسة<br/>
    <br/>
    <b>3. CSRF (Cross-Site Request Forgery):</b><br/>
    المهاجم ينشئ صفحة تنقل الأموال من حسابك<br/>
    النتيجة: تحويل أموال بدون إذن المستخدم<br/>
    <br/>
    <b>4. Weak SSL/TLS:</b><br/>
    استخدام بروتوكول SSL قديم غير آمن<br/>
    النتيجة: اختراق التشفير والوصول للبيانات المرسلة<br/>
    """
    
    elements.append(Paragraph(vulnerabilities_text, normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(PageBreak())
    
    # ========== التوصيات الأمنية ==========
    elements.append(Paragraph("🛡️ التوصيات الأمنية الأساسية", heading_style))
    
    recommendations = [
        "تحديث جميع البرامج والمكتبات بانتظام",
        "استخدام HTTPS دائماً وإجبار HTTPS عبر HSTS",
        "فلترة وتنظيف جميع المدخلات من المستخدمين",
        "استخدام Prepared Statements لقاعدة البيانات",
        "إضافة جميع رؤوس الأمان الموصى بها",
        "فعّل CSRF tokens على جميع النماذج",
        "استخدم قوية كلمات مرور و 2FA للإدارة",
        "قيّد الوصول للملفات والمجلدات الحساسة",
        "راقب السجلات (Logs) بحثاً عن أنشطة غريبة",
        "أجرِ فحوصات أمان دورية وشاملة",
    ]
    
    rec_data = [[f"✓ {rec}"] for rec in recommendations]
    
    rec_table = Table(rec_data, colWidths=[5.5*inch])
    rec_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Arabic'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f5e9')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#e8f5e9')]),
    ]))
    elements.append(rec_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ========== مقارنة مع أدوات أخرى ==========
    elements.append(Paragraph("🔀 مقارنة مع أدوات أخرى", heading_style))
    
    comparison_data = [
        ['الميزة', 'Scanner V2', 'Burp Suite', 'OWASP ZAP', 'Nessus'],
        ['السعر', 'مجاني', 'معاً (آلاف $)', 'مجاني', 'معاً'],
        ['الفحوصات', '13', '50+', '30+', '50+'],
        ['إخفاء IP', 'نعم', 'نعم', 'نعم', 'لا'],
        ['الإصلاح التلقائي', 'نعم', 'لا', 'نعم', 'نعم'],
        ['السهولة', 'سهل جداً', 'معقد', 'متوسط', 'متوسط'],
        ['الدعم العربي', 'كامل', 'محدود', 'محدود', 'لا'],
        ['Python 3', 'نعم', 'متصفح', 'Java', 'تطبيق'],
    ]
    
    comp_table = Table(comparison_data, colWidths=[1.1*inch, 1.1*inch, 1.1*inch, 1.1*inch, 1.1*inch])
    comp_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'ArabicBold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (1, 1), (1, -1), colors.HexColor('#e8f5e9')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    elements.append(comp_table)
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(PageBreak())
    
    # ========== حالات الاستخدام ==========
    elements.append(Paragraph("📊 حالات الاستخدام", heading_style))
    
    usecases_text = """
    <b>1. فريق تطوير البرمجيات (DevOps):</b><br/>
    • فحص الأمان قبل نشر التطبيق في الإنتاج<br/>
    • فحص دوري لاكتشاف الثغرات الجديدة<br/>
    • التحقق من الامتثال للمعايير الأمنية<br/>
    <br/>
    <b>2. متخصصو الأمن (Security Professionals):</b><br/>
    • اختبار الاختراق (Penetration Testing)<br/>
    • تقييم مستوى أمان التطبيقات<br/>
    • توثيق الثغرات للعملاء<br/>
    <br/>
    <b>3. مالكو المواقع (Website Owners):</b><br/>
    • التحقق من أمان موقعهم<br/>
    • اكتشاف الثغرات قبل المهاجمين<br/>
    • تلبية متطلبات الامتثال (Compliance)<br/>
    <br/>
    <b>4. الطلاب والباحثون:</b><br/>
    • تعلم الثغرات الأمنية الشهيرة<br/>
    • فهم كيفية عمل أدوات الأمان<br/>
    • بحث وتطوير تقنيات أمنية جديدة<br/>
    """
    
    elements.append(Paragraph(usecases_text, normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # ========== ملاحظات أمنية ==========
    elements.append(Paragraph("⚠️ ملاحظات أمنية هامة", heading_style))
    
    notes_text = """
    <b style="color: red;">تحذير قانوني:</b><br/>
    هذه الأداة يجب أن تُستخدم فقط على:<br/>
    • المواقع التي تملكها<br/>
    • المواقع التي لديك إذن كتابي لفحصها<br/>
    • بيئات الاختبار (Testing Environments)<br/>
    <br/>
    <b>استخدام الأداة بدون إذن قد يكون جريمة حسب القانون!</b><br/>
    <br/>
    <b>نصائح للفحص الآمن:</b><br/>
    • استخدم Proxy لإخفاء هويتك<br/>
    • تجنب الفحص على قواعد البيانات الحقيقية<br/>
    • وثّق كل ما تفعله<br/>
    • لا تقم بتعديل البيانات<br/>
    • أبلغ عن الثغرات مباشرة لمالك الموقع<br/>
    • لا تنشر الثغرات علناً بدون إصلاح<br/>
    """
    
    elements.append(Paragraph(notes_text, normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(PageBreak())
    
    # ========== المراجع والموارد ==========
    elements.append(Paragraph("📚 المراجع والموارد", heading_style))
    
    references_text = """
    <b>معايير OWASP (Open Web Application Security Project):</b><br/>
    • OWASP Top 10 - أخطر 10 ثغرات ويب<br/>
    • OWASP Testing Guide - دليل اختبار الأمان<br/>
    • OWASP Cheat Sheets - نماذج سريعة للأمان<br/>
    <br/>
    <b>المعايير الدولية:</b><br/>
    • ISO 27001 - معايير الأمان المعلومات<br/>
    • NIST Cybersecurity Framework - إطار عمل الأمان<br/>
    • PCI DSS - معايير أمان بطاقات الائتمان<br/>
    <br/>
    <b>مواقع مفيدة:</b><br/>
    • https://owasp.org - موقع OWASP الرسمي<br/>
    • https://cve.mitre.org - قاعدة الثغرات المعروفة<br/>
    • https://nvd.nist.gov - قاعدة الثغرات الوطنية<br/>
    • https://web.dev/security - أدلة أمان الويب<br/>
    <br/>
    <b>المجتمعات الأمنية:</b><br/>
    • HackerOne - منصة تقارير الثغرات<br/>
    • Bugcrowd - برنامج مكافأة الثغرات<br/>
    • Stack Exchange Security - مجتمع أسئلة الأمان<br/>
    """
    
    elements.append(Paragraph(references_text, normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # ========== الخلاصة ==========
    elements.append(PageBreak())
    elements.append(Paragraph("✅ الخلاصة", heading_style))
    
    conclusion_text = """
    أداة فحص أمان المواقع المتقدمة (Scanner V2) توفر حلاً شاملاً وسهل الاستخدام لفحص أمان تطبيقات الويب.
    بـ 13 فحص متقدم وميزات مثل إخفاء IP والإصلاح التلقائي، تُعتبر الأداة مثالية للمطورين والمتخصصين الأمنيين.<br/>
    <br/>
    <b>المميزات الرئيسية:</b><br/>
    ✓ مجانية وسهلة الاستخدام<br/>
    ✓ 13 فحص شامل<br/>
    ✓ إخفاء IP متقدم<br/>
    ✓ إصلاح ذكي<br/>
    ✓ دعم عربي كامل<br/>
    ✓ تقارير منظمة<br/>
    <br/>
    <b>التوصيات النهائية:</b><br/>
    1. استخدم الأداة بانتظام لفحص أمان تطبيقاتك<br/>
    2. اتبع التوصيات والإصلاحات المقترحة<br/>
    3. حدّث الأداة للحصول على أحدث الفحوصات<br/>
    4. شارك الأداة مع فريقك<br/>
    5. تعاون مع متخصصي الأمان<br/>
    <br/>
    <b>تذكر: الأمان عملية مستمرة، وليس حدث واحد!</b>
    """
    
    elements.append(Paragraph(conclusion_text, normal_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # ========== معلومات التقرير النهائية ==========
    footer_data = [
        ['تم إنشاء التقرير بواسطة:', 'Advanced Web Security Scanner V2'],
        ['تاريخ الإنشاء:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['الإصدار:', '2.0'],
        ['اللغة:', 'العربية'],
    ]
    
    footer_table = Table(footer_data, colWidths=[2*inch, 3*inch])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (0, -1), 'ArabicBold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
    ]))
    elements.append(footer_table)
    
    # بناء المستند
    doc.build(elements)
    
    return filename

if __name__ == "__main__":
    filename = create_security_scanner_report()
    print(f"\n✅ تم إنشاء التقرير بنجاح!")
    print(f"📄 اسم الملف: {filename}")
    print(f"📊 نوع الملف: PDF")
    print(f"🌍 اللغة: العربية بالكامل")
    print(f"📋 الحجم: أكثر من 10 صفحات")
