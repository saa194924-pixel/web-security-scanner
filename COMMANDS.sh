#!/bin/bash
# أوامر فحص أمان المواقع الشاملة
# Web Security Scanner Commands
# ==============================

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🔐 أوامر فحص أمان المواقع الشاملة                       ║"
echo "║  Web Security Scanner - Complete Commands                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# ============ الأوامر الأساسية ============
echo "📋 الأوامر الأساسية - Basic Commands:"
echo "========================================="
echo ""

echo "1️⃣ فحص شامل كامل (Gobuster + Nmap + Leaked Files):"
echo "   python3 main.py -t example.com -a"
echo ""

echo "2️⃣ فحص Gobuster (المجلدات والملفات):"
echo "   python3 main.py -t example.com --gobuster"
echo "   أو: gobuster dir -u https://example.com -w wordlist.txt"
echo ""

echo "3️⃣ فحص Nmap (المنافذ والخدمات):"
echo "   python3 main.py -t example.com --nmap"
echo "   أو: nmap -p- -sV -A example.com"
echo ""

echo "4️⃣ فحص الملفات المسربة:"
echo "   python3 main.py -t example.com --leaked"
echo ""

# ============ الأوامر المتقدمة ============
echo ""
echo "🔥 الأوامر المتقدمة - Advanced Commands:"
echo "========================================"
echo ""

echo "🎯 فحص عدواني شامل (احذر - قد يستغرق وقتًا طويلًا):"
echo "   python3 main.py -t example.com -a --aggressive"
echo ""

echo "📊 فحص مع تفاصيل عالية:"
echo "   python3 main.py -t example.com -a -v"
echo ""

# ============ أوامر Gobuster المباشرة ============
echo ""
echo "🚀 أوامر Gobuster المباشرة - Gobuster Direct Commands:"
echo "======================================================"
echo ""

echo "🔍 فحص المجلدات بسرعة عالية:"
echo "   gobuster dir -u https://example.com -w wordlist.txt -t 100 -s 200,301,302,401,403"
echo ""

echo "🔍 فحص المجلدات مع امتدادات:"
echo "   gobuster dir -u https://example.com -w wordlist.txt -x php,html,txt,xml,json,bak -t 100"
echo ""

echo "🔍 فحص بحثًا عن API endpoints:"
echo "   gobuster dir -u https://example.com/api -w api_wordlist.txt -t 100"
echo ""

echo "🔍 فحص DNS (النطاقات الفرعية):"
echo "   gobuster dns -d example.com -w subdomains.txt -t 100"
echo ""

echo "🔍 فحص VHost (Virtual Hosts):"
echo "   gobuster vhost -u https://example.com -w vhosts.txt -t 100"
echo ""

# ============ أوامر Nmap المباشرة ============
echo ""
echo "🔥 أوامر Nmap المباشرة - Nmap Direct Commands:"
echo "=============================================="
echo ""

echo "🎯 فحص شامل جميع المنافذ 0-65535:"
echo "   nmap -p- -sS -T4 --open example.com"
echo ""

echo "🎯 فحص المنافذ مع كشف الخدمات والإصدارات:"
echo "   nmap -sV -sC -O -A example.com"
echo ""

echo "🎯 فحص الثغرات الأمنية (NSE vuln scripts):"
echo "   nmap --script vuln -sV example.com"
echo ""

echo "🎯 فحص عدواني شامل جداً:"
echo "   nmap -p- -A -T5 --script default,vuln -sV -O example.com"
echo ""

echo "🎯 فحص شامل مع حفظ النتائج:"
echo "   nmap -p- -sV -A --script vuln -oX report.xml -oG report.gnmap example.com"
echo ""

echo "🎯 فحص المنافذ المشبوهة فقط:"
echo "   nmap -p 3128,8008,8888,9000,27017,5432,3306,6379 -sV example.com"
echo ""

echo "🎯 فحص نظام التشغيل (OS detection):"
echo "   nmap -O --osscan-guess example.com"
echo ""

echo "🎯 فحص مع إخفاء IP (يتطلب root):"
echo "   sudo nmap -sV -T2 -p- --randomize-hosts -D RND:10 example.com"
echo ""

# ============ أوامر البحث عن الملفات المسربة ============
echo ""
echo "🚨 أوامر البحث عن الملفات المسربة - Leaked Files Search:"
echo "======================================================"
echo ""

echo "🔎 البحث عن .env:"
echo "   curl https://example.com/.env"
echo "   wget https://example.com/.env"
echo ""

echo "🔎 البحث عن config.php:"
echo "   curl https://example.com/config.php"
echo ""

echo "🔎 البحث عن قاعدة البيانات:"
echo "   wget https://example.com/database.sql"
echo "   wget https://example.com/database.db"
echo ""

echo "🔎 البحث عن مفاتيح SSH:"
echo "   curl https://example.com/id_rsa"
echo "   curl https://example.com/.ssh/id_rsa"
echo ""

echo "🔎 البحث عن backup.zip:"
echo "   wget https://example.com/backup.zip"
echo ""

echo "🔎 البحث عن wp-config.php:"
echo "   curl https://example.com/wp-config.php.bak"
echo ""

# ============ أوامر مساعدة ============
echo ""
echo "🛠️ أوامر مساعدة - Utility Commands:"
echo "===================================="
echo ""

echo "📥 تثبيت المتطلبات:"
echo "   pip install -r requirements.txt"
echo ""

echo "🔧 تثبيت Gobuster:"
echo "   sudo apt-get install gobuster"
echo "   brew install gobuster"
echo "   go install github.com/OJ/gobuster/v3@latest"
echo ""

echo "🔧 تثبيت Nmap:"
echo "   sudo apt-get install nmap"
echo "   brew install nmap"
echo ""

echo "📋 عرض مساعدة أدوات Gobuster:"
echo "   gobuster --help"
echo "   gobuster dir --help"
echo "   gobuster dns --help"
echo ""

echo "📋 عرض مساعدة أدوات Nmap:"
echo "   nmap --help"
echo "   nmap --script-help=vuln"
echo ""

# ============ السيناريوهات المشهورة ============
echo ""
echo "⭐ السيناريوهات المشهورة - Popular Scenarios:"
echo "=========================================="
echo ""

echo "📌 سيناريو 1: فحص موقع WordPress كامل:"
echo "   python3 main.py -t example.com -a"
echo "   gobuster dir -u https://example.com -w wordlists/wordpress.txt -x php"
echo "   curl https://example.com/wp-config.php.bak"
echo ""

echo "📌 سيناريو 2: فحص API:"
echo "   python3 main.py -t api.example.com -a"
echo "   gobuster dir -u https://api.example.com -w wordlists/api.txt"
echo "   nmap -sV -p 8000-9000 api.example.com"
echo ""

echo "📌 سيناريو 3: فحص بحثًا عن بيانات مسربة:"
echo "   python3 main.py -t example.com --leaked"
echo "   curl https://example.com/.env"
echo "   curl https://example.com/.git/config"
echo ""

echo "📌 سيناريو 4: فحص شامل عدواني (احذر!):"
echo "   sudo python3 main.py -t example.com -a --aggressive"
echo ""

# ============ نصائح المهمة ============
echo ""
echo "⚠️ نصائح المهمة - Important Tips:"
echo "=================================="
echo ""

echo "✓ استخدم -v أو --verbose للحصول على مزيد من التفاصيل"
echo "✓ حفظ النتائج باستخدام -oX, -oG, -oN مع nmap"
echo "✓ استخدم -T4 مع nmap لسرعة أفضل"
echo "✓ قد تحتاج إلى sudo/root لبعض الفحوصات المتقدمة"
echo "✓ تأكد من حصولك على إذن قبل اختبار أي موقع"
echo "✓ استخدم VPN عند الاختبار على مواقع إنتاجية"
echo ""

echo "════════════════════════════════════════════════════════════"
echo "✅ لمزيد من المعلومات: python3 main.py -h"
echo "════════════════════════════════════════════════════════════"
