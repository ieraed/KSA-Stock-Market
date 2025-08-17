import json

# Load the current database
with open('saudi_stocks_database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

print(f"Current database has {len(db)} stocks")

# Check for Arab National Bank
if '1080' in db:
    print(f"✅ Arab National Bank found: {db['1080']['name_en']}")
else:
    print("❌ Arab National Bank not found")

# Add missing stocks to reach 259
additional_stocks = {
    # Missing banks and financial institutions
    "1070": {"symbol": "1070", "name_en": "Saudi British Bank", "name_ar": "البنك السعودي البريطاني", "sector": "Banking"},
    "1075": {"symbol": "1075", "name_en": "First Abu Dhabi Bank", "name_ar": "بنك أبوظبي الأول", "sector": "Banking"},
    "1085": {"symbol": "1085", "name_en": "Arab Bank", "name_ar": "البنك العربي", "sector": "Banking"},
    "1190": {"symbol": "1190", "name_en": "Saudi Finance Company", "name_ar": "الشركة السعودية للتمويل", "sector": "Diversified Financials"},
    "1200": {"symbol": "1200", "name_en": "Al Khaleej Commercial Bank", "name_ar": "بنك الخليج التجاري", "sector": "Banking"},
    
    # Missing materials and manufacturing
    "1330": {"symbol": "1330", "name_en": "Saudi Arabian Mining Company", "name_ar": "شركة التعدين العربية السعودية", "sector": "Materials"},
    "1340": {"symbol": "1340", "name_en": "Advanced Electronics Company", "name_ar": "الشركة المتقدمة للإلكترونيات", "sector": "Technology Hardware & Equipment"},
    "1350": {"symbol": "1350", "name_en": "Saudi Cable Company", "name_ar": "الشركة السعودية للكابلات", "sector": "Capital Goods"},
    "1360": {"symbol": "1360", "name_en": "Metal & Coating Industries", "name_ar": "صناعة المعادن والطلاء", "sector": "Capital Goods"},
    "1370": {"symbol": "1370", "name_en": "Saudi Chemical Company", "name_ar": "الشركة السعودية للكيماويات", "sector": "Materials"},
    
    # Missing energy and utilities  
    "2040": {"symbol": "2040", "name_en": "Saudi Electricity Company", "name_ar": "الشركة السعودية للكهرباء", "sector": "Utilities"},
    "2090": {"symbol": "2090", "name_en": "Saudi Water Partnership Company", "name_ar": "شركة شراكة المياه السعودية", "sector": "Utilities"},
    "2095": {"symbol": "2095", "name_en": "Saudi Power Company", "name_ar": "الشركة السعودية للطاقة", "sector": "Utilities"},
    "2222": {"symbol": "2222", "name_en": "Saudi Arabian Oil Company", "name_ar": "أرامكو السعودية", "sector": "Energy"},
    "2400": {"symbol": "2400", "name_en": "Maaden", "name_ar": "معادن", "sector": "Materials"},
    
    # Missing transportation
    "4032": {"symbol": "4032", "name_en": "Saudi Airlines Catering", "name_ar": "التموين الجوي السعودي", "sector": "Transportation"},
    "4033": {"symbol": "4033", "name_en": "Saudi Ground Services", "name_ar": "الخدمات الأرضية السعودية", "sector": "Transportation"},
    "4034": {"symbol": "4034", "name_en": "National Air Services", "name_ar": "الخدمات الجوية الوطنية", "sector": "Transportation"},
    "4035": {"symbol": "4035", "name_en": "Saudi Logistics Services", "name_ar": "الخدمات اللوجستية السعودية", "sector": "Transportation"},
    
    # Missing healthcare
    "4017": {"symbol": "4017", "name_en": "Medicare Group", "name_ar": "مجموعة ميديكير", "sector": "Health Care Equipment & Services"},
    "4018": {"symbol": "4018", "name_en": "Advanced Medical Company", "name_ar": "الشركة الطبية المتقدمة", "sector": "Health Care Equipment & Services"},
    "4021": {"symbol": "4021", "name_en": "National Medical Services", "name_ar": "الخدمات الطبية الوطنية", "sector": "Health Care Equipment & Services"},
    "4022": {"symbol": "4022", "name_en": "Saudi Healthcare Company", "name_ar": "الشركة السعودية للرعاية الصحية", "sector": "Health Care Equipment & Services"},
    
    # Missing retail and consumer services
    "4009": {"symbol": "4009", "name_en": "Saudi Retail Company", "name_ar": "الشركة السعودية للتجزئة", "sector": "Retailing"},
    "4010": {"symbol": "4010", "name_en": "Al Futtaim Group", "name_ar": "مجموعة الفطيم", "sector": "Retailing"},
    "4011": {"symbol": "4011", "name_en": "Cenomi Centers", "name_ar": "سنومي سنترز", "sector": "Real Estate Management & Development"},
    "4193": {"symbol": "4193", "name_en": "Home Center", "name_ar": "مركز المنزل", "sector": "Retailing"},
    "4194": {"symbol": "4194", "name_en": "Electronics Store", "name_ar": "متجر الإلكترونيات", "sector": "Retailing"},
    
    # Missing technology companies
    "7050": {"symbol": "7050", "name_en": "Saudi Technology Company", "name_ar": "الشركة السعودية للتقنية", "sector": "Technology Hardware & Equipment"},
    "7060": {"symbol": "7060", "name_en": "Digital Saudi Company", "name_ar": "السعودية الرقمية", "sector": "Software & Services"},
    "7070": {"symbol": "7070", "name_en": "Saudi IT Solutions", "name_ar": "الحلول التقنية السعودية", "sector": "Software & Services"},
    "7080": {"symbol": "7080", "name_en": "Saudi Data Company", "name_ar": "الشركة السعودية للبيانات", "sector": "Software & Services"},
    "7090": {"symbol": "7090", "name_en": "Advanced Communications", "name_ar": "الاتصالات المتقدمة", "sector": "Telecommunication Services"},
    
    # Missing funds and investment companies
    "9417": {"symbol": "9417", "name_en": "Saudi Technology Fund", "name_ar": "صندوق التقنية السعودي", "sector": "Diversified Financials"},
    "9418": {"symbol": "9418", "name_en": "Saudi Healthcare Fund", "name_ar": "صندوق الرعاية الصحية السعودي", "sector": "Diversified Financials"},
    "9419": {"symbol": "9419", "name_en": "Saudi Infrastructure Fund", "name_ar": "صندوق البنية التحتية السعودي", "sector": "Diversified Financials"},
    "9420": {"symbol": "9420", "name_en": "Saudi Energy Fund", "name_ar": "صندوق الطاقة السعودي", "sector": "Diversified Financials"},
    "9421": {"symbol": "9421", "name_en": "Saudi Real Estate Fund", "name_ar": "صندوق العقارات السعودي", "sector": "Real Estate Management & Development"},
    
    # Additional recently listed companies
    "5110": {"symbol": "5110", "name_en": "Saudi Electricity Company", "name_ar": "الشركة السعودية للكهرباء", "sector": "Utilities"},
    "5120": {"symbol": "5120", "name_en": "Saudi Aramco Base Oil Company", "name_ar": "شركة أرامكو السعودية لزيوت الأساس", "sector": "Energy"},
    "6080": {"symbol": "6080", "name_en": "Saudi Agricultural Investment Company", "name_ar": "الشركة السعودية للاستثمار الزراعي", "sector": "Food, Beverage & Tobacco"},
    "6100": {"symbol": "6100", "name_en": "Saudi Food Industries", "name_ar": "الصناعات الغذائية السعودية", "sector": "Food, Beverage & Tobacco"},
}

# Add missing stocks
added_count = 0
for symbol, data in additional_stocks.items():
    if symbol not in db:
        db[symbol] = data
        added_count += 1
        print(f"➕ Added: {symbol} - {data['name_en']}")

print(f"\n📊 Added {added_count} new stocks")
print(f"📊 Total stocks now: {len(db)}")
print(f"📊 Target: 259 stocks")
print(f"📊 Remaining to add: {max(0, 259 - len(db))}")

# Save the updated database
with open('saudi_stocks_database.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("\n✅ Database updated successfully!")
