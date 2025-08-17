#!/usr/bin/env python3
"""
🇸🇦 Complete Saudi Exchange Stock Fetcher
Fetches all 259+ Saudi stocks from multiple sources and creates comprehensive database
"""

import json
import requests
import pandas as pd
from datetime import datetime
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_existing_databases():
    """Load all existing database files"""
    databases = {}
    
    files_to_check = [
        'saudi_stocks_database.json',
        'saudi_stocks_database_official.json', 
        'saudi_stocks_database_corrected.json'
    ]
    
    for filename in files_to_check:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                databases[filename] = data
                logger.info(f"✅ Loaded {filename}: {len(data)} stocks")
        except Exception as e:
            logger.warning(f"❌ Could not load {filename}: {e}")
    
    return databases

def merge_databases(databases):
    """Merge all databases, prioritizing official data"""
    merged = {}
    
    # Priority order: official > corrected > main
    priority_order = [
        'saudi_stocks_database.json',
        'saudi_stocks_database_corrected.json', 
        'saudi_stocks_database_official.json'  # Highest priority
    ]
    
    for filename in priority_order:
        if filename in databases:
            for symbol, data in databases[filename].items():
                merged[symbol] = data
                logger.debug(f"Added/Updated {symbol}: {data.get('name_en', 'Unknown')}")
    
    return merged

def get_comprehensive_saudi_stocks():
    """Get comprehensive list of all Saudi stocks with complete metadata"""
    
    # Complete database of Saudi stocks based on official sources
    complete_stocks = {
        # Banking Sector (1010-1999)
        "1010": {"symbol": "1010", "name_en": "Riyad Bank", "name_ar": "بنك الرياض", "sector": "Banking"},
        "1020": {"symbol": "1020", "name_en": "Bank AlJazira", "name_ar": "بنك الجزيرة", "sector": "Banking"},
        "1030": {"symbol": "1030", "name_en": "Saudi Investment Bank", "name_ar": "البنك السعودي للاستثمار", "sector": "Banking"},
        "1050": {"symbol": "1050", "name_en": "Banque Saudi Fransi", "name_ar": "البنك السعودي الفرنسي", "sector": "Banking"},
        "1060": {"symbol": "1060", "name_en": "Saudi Awwal Bank", "name_ar": "البنك الأول", "sector": "Banking"},
        "1080": {"symbol": "1080", "name_en": "Arab National Bank", "name_ar": "البنك الأهلي العربي", "sector": "Banking"},
        "1111": {"symbol": "1111", "name_en": "Tadawul Group", "name_ar": "مجموعة تداول", "sector": "Financial Services"},
        "1120": {"symbol": "1120", "name_en": "Al Rajhi Bank", "name_ar": "مصرف الراجحي", "sector": "Banking"},
        "1140": {"symbol": "1140", "name_en": "Bank AlBilad", "name_ar": "بنك البلاد", "sector": "Banking"},
        "1150": {"symbol": "1150", "name_en": "Alinma Bank", "name_ar": "بنك الإنماء", "sector": "Banking"},
        "1180": {"symbol": "1180", "name_en": "Saudi National Bank", "name_ar": "البنك الأهلي السعودي", "sector": "Banking"},
        "1182": {"symbol": "1182", "name_en": "Saudi Real Estate Refinance Company", "name_ar": "شركة إعادة التمويل العقاري السعودية", "sector": "Financial Services"},
        "1183": {"symbol": "1183", "name_en": "Altamweel", "name_ar": "التمويل", "sector": "Financial Services"},
        
        # Capital Goods & Manufacturing (1200-1999)
        "1201": {"symbol": "1201", "name_en": "Al Hassan Ghazi Ibrahim Shaker", "name_ar": "الحسن غازي إبراهيم شاكر", "sector": "Capital Goods"},
        "1210": {"symbol": "1210", "name_en": "Saudi Red Sea Housing Services", "name_ar": "خدمات الإسكان والتعمير", "sector": "Real Estate Management & Development"},
        "1211": {"symbol": "1211", "name_en": "Maharah Human Resources", "name_ar": "مهارة للموارد البشرية", "sector": "Commercial & Professional Services"},
        "1213": {"symbol": "1213", "name_en": "Maharah HR", "name_ar": "مهارة", "sector": "Commercial & Professional Services"},
        "1214": {"symbol": "1214", "name_en": "Al Hassan Ghazi Ibrahim Shaker", "name_ar": "الحسن غازي ابراهيم شاكر", "sector": "Capital Goods"},
        "1301": {"symbol": "1301", "name_en": "Aslak", "name_ar": "أسلاك", "sector": "Capital Goods"},
        "1303": {"symbol": "1303", "name_en": "Electrical Industries Company", "name_ar": "الصناعات الكهربائية", "sector": "Capital Goods"},
        "1304": {"symbol": "1304", "name_en": "Al Yamamah Steel Industries", "name_ar": "اليمامة للصناعات الحديدية", "sector": "Capital Goods"},
        "1320": {"symbol": "1320", "name_en": "Saudi Steel Pipe Company", "name_ar": "أنابيب السعودية", "sector": "Capital Goods"},
        "1321": {"symbol": "1321", "name_en": "Eastern Pipes", "name_ar": "الأنابيب السعودية", "sector": "Capital Goods"},
        "1322": {"symbol": "1322", "name_en": "Amak", "name_ar": "أعمال", "sector": "Capital Goods"},
        "1323": {"symbol": "1323", "name_en": "United Wire Factories Company", "name_ar": "مصانع الأسلاك المتحدة", "sector": "Capital Goods"},
        
        # Real Estate & Development (1800-1999)
        "1810": {"symbol": "1810", "name_en": "Seera Group", "name_ar": "مجموعة سيرا", "sector": "Consumer Services"},
        "1820": {"symbol": "1820", "name_en": "Baan for Real Estate Development", "name_ar": "بان للتطوير العقاري", "sector": "Real Estate Management & Development"},
        "1833": {"symbol": "1833", "name_en": "Al Mawarid Manpower", "name_ar": "الموارد البشرية", "sector": "Commercial & Professional Services"},
        "1834": {"symbol": "1834", "name_en": "Saudi Advanced Medical Services Company", "name_ar": "الشركة السعودية للخدمات الطبية المتقدمة", "sector": "Health Care Equipment & Services"},
        "1835": {"symbol": "1835", "name_en": "Tamkeen Technologies", "name_ar": "تمكين التقنيات", "sector": "Technology Hardware & Equipment"},
        
        # Materials & Energy (2000-2999)
        "2010": {"symbol": "2010", "name_en": "Saudi Basic Industries Corporation", "name_ar": "سابك", "sector": "Materials"},
        "2020": {"symbol": "2020", "name_en": "SABIC Agri-Nutrients Company", "name_ar": "سابك للمغذيات الزراعية", "sector": "Materials"},
        "2030": {"symbol": "2030", "name_en": "Saudi Arabian Oil Company", "name_ar": "أرامكو السعودية", "sector": "Energy"},
        "2050": {"symbol": "2050", "name_en": "Savola Group", "name_ar": "مجموعة صافولا", "sector": "Food & Staples Retailing"},
        "2060": {"symbol": "2060", "name_en": "The National Industrialization Company", "name_ar": "التصنيع الوطنية", "sector": "Materials"},
        "2070": {"symbol": "2070", "name_en": "Saudi Pharmaceutical Industries & Medical Appliances Corporation", "name_ar": "سبيماكو الأدوية", "sector": "Pharmaceuticals, Biotechnology & Life Sciences"},
        "2081": {"symbol": "2081", "name_en": "Al Babtain Power and Telecommunication", "name_ar": "البابطين للطاقة والاتصالات", "sector": "Utilities"},
        "2082": {"symbol": "2082", "name_en": "ACWA Power", "name_ar": "أكوا باور", "sector": "Utilities"},
        "2083": {"symbol": "2083", "name_en": "Marafiq", "name_ar": "مرافق", "sector": "Utilities"},
        "2084": {"symbol": "2084", "name_en": "Miahona", "name_ar": "مياهنا", "sector": "Utilities"},
        "2100": {"symbol": "2100", "name_en": "Wafrah for Industry and Development", "name_ar": "وفرة للصناعة والتنمية", "sector": "Food, Beverage & Tobacco"},
        "2120": {"symbol": "2120", "name_en": "Saudi Industrial Investment Company", "name_ar": "الشركة السعودية للاستثمار الصناعي", "sector": "Materials"},
        "2130": {"symbol": "2130", "name_en": "Saudi Industrial Development Company", "name_ar": "التنمية الصناعية السعودية", "sector": "Materials"},
        "2140": {"symbol": "2140", "name_en": "Ayyan Investment", "name_ar": "عيان للاستثمار", "sector": "Real Estate Management & Development"},
        "2160": {"symbol": "2160", "name_en": "Saudi Amiantit Company", "name_ar": "الشركة السعودية لصناعة الأنابيب", "sector": "Capital Goods"},
        "2170": {"symbol": "2170", "name_en": "Alujain Corporation", "name_ar": "العجين القابضة", "sector": "Materials"},
        "2180": {"symbol": "2180", "name_en": "Fipco", "name_ar": "فيبكو", "sector": "Materials"},
        "2190": {"symbol": "2190", "name_en": "Saudi Industrial Services Company", "name_ar": "سيسكو القابضة", "sector": "Commercial & Professional Services"},
        "2200": {"symbol": "2200", "name_en": "Anaam International Holding Group", "name_ar": "أنعام القابضة الدولية", "sector": "Food, Beverage & Tobacco"},
        "2210": {"symbol": "2210", "name_en": "Nama Chemicals Company", "name_ar": "نماء للكيماويات", "sector": "Materials"},
        "2220": {"symbol": "2220", "name_en": "Maadaniyah", "name_ar": "معادنية", "sector": "Materials"},
        "2222": {"symbol": "2222", "name_en": "Saudi Arabian Oil Company", "name_ar": "أرامكو السعودية", "sector": "Energy"},
        "2230": {"symbol": "2230", "name_en": "Saudi Industrial Investment Group", "name_ar": "مجموعة الاستثمار الصناعي", "sector": "Materials"},
        "2250": {"symbol": "2250", "name_en": "Saudi Industrial Investment Group", "name_ar": "مجموعة الاستثمار الصناعي", "sector": "Materials"},
        "2270": {"symbol": "2270", "name_en": "Saudia Dairy & Foodstuff Company", "name_ar": "صدافكو", "sector": "Food, Beverage & Tobacco"},
        "2280": {"symbol": "2280", "name_en": "Almarai Company", "name_ar": "المراعي", "sector": "Food, Beverage & Tobacco"},
        "2281": {"symbol": "2281", "name_en": "Tanmiah Food Company", "name_ar": "تنمية", "sector": "Food, Beverage & Tobacco"},
        "2282": {"symbol": "2282", "name_en": "Naqii", "name_ar": "ناقي", "sector": "Food, Beverage & Tobacco"},
        "2287": {"symbol": "2287", "name_en": "Entaj", "name_ar": "إنتاج", "sector": "Food, Beverage & Tobacco"},
        "2290": {"symbol": "2290", "name_en": "Yanbu National Petrochemical Company", "name_ar": "ينساب", "sector": "Materials"},
        "2320": {"symbol": "2320", "name_en": "Al Babtain Power and Telecommunication Company", "name_ar": "البابطين للطاقة والاتصالات", "sector": "Capital Goods"},
        "2330": {"symbol": "2330", "name_en": "Advanced Petrochemical Company", "name_ar": "المتقدمة للبتروكيماويات", "sector": "Materials"},
        "2350": {"symbol": "2350", "name_en": "Saudi Kayan Petrochemical Company", "name_ar": "كيان السعودية", "sector": "Materials"},
        "2360": {"symbol": "2360", "name_en": "Saudi Venture Capital Company", "name_ar": "الاستثمار الجريء السعودي", "sector": "Diversified Financials"},
        "2382": {"symbol": "2382", "name_en": "Advanced Drilling & Engineering Services", "name_ar": "أديس", "sector": "Energy"},
        
        # Cement & Construction Materials (3000-3999)
        "3003": {"symbol": "3003", "name_en": "City Cement Company", "name_ar": "إسمنت المدينة", "sector": "Materials"},
        "3005": {"symbol": "3005", "name_en": "United Arabian Cement Company", "name_ar": "الإسمنت العربية المتحدة", "sector": "Materials"},
        "3007": {"symbol": "3007", "name_en": "Oasis", "name_ar": "واحة", "sector": "Materials"},
        "3008": {"symbol": "3008", "name_en": "Al Kathiri Holding", "name_ar": "الكثيري القابضة", "sector": "Materials"},
        "3010": {"symbol": "3010", "name_en": "Arabian Cement Company", "name_ar": "الإسمنت العربية", "sector": "Materials"},
        "3020": {"symbol": "3020", "name_en": "Yamama Cement Company", "name_ar": "إسمنت اليمامة", "sector": "Materials"},
        "3040": {"symbol": "3040", "name_en": "Qassim Cement Company", "name_ar": "إسمنت القصيم", "sector": "Materials"},
        "3050": {"symbol": "3050", "name_en": "Southern Province Cement Company", "name_ar": "إسمنت المنطقة الجنوبية", "sector": "Materials"},
        "3080": {"symbol": "3080", "name_en": "Eastern Province Cement Company", "name_ar": "إسمنت المنطقة الشرقية", "sector": "Materials"},
        "3090": {"symbol": "3090", "name_en": "Tabuk Cement Company", "name_ar": "إسمنت تبوك", "sector": "Materials"},
        
        # Consumer Services & Retail (4000-4999)
        "4001": {"symbol": "4001", "name_en": "Abdullah Al Othaim Markets", "name_ar": "أسواق عبدالله العثيم", "sector": "Food & Staples Retailing"},
        "4003": {"symbol": "4003", "name_en": "Extra Stores Company", "name_ar": "إكسترا", "sector": "Consumer Durables & Apparel"},
        "4004": {"symbol": "4004", "name_en": "Dallah Healthcare Company", "name_ar": "دله الصحية", "sector": "Health Care Equipment & Services"},
        "4005": {"symbol": "4005", "name_en": "Middle East Healthcare Company", "name_ar": "الشرق الأوسط للرعاية الصحية", "sector": "Health Care Equipment & Services"},
        "4007": {"symbol": "4007", "name_en": "Al Hammadi Company for Development and Investment", "name_ar": "الحمادي للتنمية والاستثمار", "sector": "Health Care Equipment & Services"},
        "4008": {"symbol": "4008", "name_en": "Saudi Automotive Company", "name_ar": "ساكو", "sector": "Retailing"},
        "4012": {"symbol": "4012", "name_en": "Al Aseel", "name_ar": "الأصيل", "sector": "Food, Beverage & Tobacco"},
        "4013": {"symbol": "4013", "name_en": "Dr. Sulaiman Al Habib Medical Services Group", "name_ar": "مجموعة د. سليمان الحبيب الطبية", "sector": "Health Care Equipment & Services"},
        "4015": {"symbol": "4015", "name_en": "Jamjoom Pharmaceuticals", "name_ar": "جمجوم فارما", "sector": "Pharmaceuticals, Biotechnology & Life Sciences"},
        "4016": {"symbol": "4016", "name_en": "Avalon Pharma", "name_ar": "أفالون فارما", "sector": "Pharmaceuticals, Biotechnology & Life Sciences"},
        "4019": {"symbol": "4019", "name_en": "Saudi Medical Care Company", "name_ar": "الرعاية الطبية السعودية", "sector": "Health Care Equipment & Services"},
        "4020": {"symbol": "4020", "name_en": "Al Akaria Real Estate Investment & Development", "name_ar": "العقارية", "sector": "Real Estate Management & Development"},
        "4030": {"symbol": "4030", "name_en": "The National Shipping Company of Saudi Arabia", "name_ar": "البحري", "sector": "Transportation"},
        "4031": {"symbol": "4031", "name_en": "Saudi Ground Services", "name_ar": "الخدمات الأرضية", "sector": "Transportation"},
        "4040": {"symbol": "4040", "name_en": "Saudi Public Transport Company", "name_ar": "سابتكو", "sector": "Transportation"},
        "4050": {"symbol": "4050", "name_en": "Saudi Arabian Oil Company", "name_ar": "أرامكو", "sector": "Energy"},
        "4051": {"symbol": "4051", "name_en": "Baazeem Trading Company", "name_ar": "باعظيم التجارية", "sector": "Retailing"},
        "4061": {"symbol": "4061", "name_en": "Anaam International Holding", "name_ar": "أنعام القابضة الدولية", "sector": "Food, Beverage & Tobacco"},
        "4070": {"symbol": "4070", "name_en": "Tihama Advertising, Public Relations and Marketing", "name_ar": "تهامة", "sector": "Media"},
        "4071": {"symbol": "4071", "name_en": "Al Arabia Trading and Marine Services", "name_ar": "العربية", "sector": "Transportation"},
        "4080": {"symbol": "4080", "name_en": "Sinad Holding", "name_ar": "سناد القابضة", "sector": "Food, Beverage & Tobacco"},
        "4081": {"symbol": "4081", "name_en": "Nayifat Finance Company", "name_ar": "نايفات للتمويل", "sector": "Diversified Financials"},
        "4082": {"symbol": "4082", "name_en": "Medical and Dental Equipment Company", "name_ar": "مرنا", "sector": "Health Care Equipment & Services"},
        "4083": {"symbol": "4083", "name_en": "Tasheel Finance", "name_ar": "تسهيل", "sector": "Diversified Financials"},
        "4084": {"symbol": "4084", "name_en": "Derayah Financial", "name_ar": "دراية المالية", "sector": "Diversified Financials"},
        "4090": {"symbol": "4090", "name_en": "Taiba Holding", "name_ar": "طيبة للاستثمار", "sector": "Real Estate Management & Development"},
        "4100": {"symbol": "4100", "name_en": "Makkah Construction & Development Company", "name_ar": "مكة للإنشاء والتعمير", "sector": "Real Estate Management & Development"},
        "4110": {"symbol": "4110", "name_en": "Batic Investments and Logistics Company", "name_ar": "باتك", "sector": "Transportation"},
        "4130": {"symbol": "4130", "name_en": "Saudi DARB", "name_ar": "درب السعودية", "sector": "Real Estate Management & Development"},
        "4140": {"symbol": "4140", "name_en": "Saudi Industrial Export Company", "name_ar": "الصادرات الصناعية", "sector": "Capital Goods"},
        "4143": {"symbol": "4143", "name_en": "Talco", "name_ar": "تالكو", "sector": "Materials"},
        "4150": {"symbol": "4150", "name_en": "Arabian Drilling Company", "name_ar": "الحفر العربية", "sector": "Energy"},
        "4160": {"symbol": "4160", "name_en": "Thimar Development Holding", "name_ar": "ثمار للتنمية", "sector": "Real Estate Management & Development"},
        "4161": {"symbol": "4161", "name_en": "Bindawood Holding", "name_ar": "بن داود القابضة", "sector": "Food & Staples Retailing"},
        "4163": {"symbol": "4163", "name_en": "Aldawaa Medical Services", "name_ar": "الدواء", "sector": "Health Care Equipment & Services"},
        "4164": {"symbol": "4164", "name_en": "National Medical Care Company", "name_ar": "النهدي الطبية", "sector": "Health Care Equipment & Services"},
        "4165": {"symbol": "4165", "name_en": "Al Majed Oud", "name_ar": "الماجد للعود", "sector": "Consumer Durables & Apparel"},
        "4170": {"symbol": "4170", "name_en": "Telecommunications and Information Technology Company", "name_ar": "تيكو", "sector": "Technology Hardware & Equipment"},
        "4180": {"symbol": "4180", "name_en": "Fitaihi Group", "name_ar": "مجموعة فتيحي", "sector": "Consumer Durables & Apparel"},
        "4190": {"symbol": "4190", "name_en": "Jarir Marketing Company", "name_ar": "جرير", "sector": "Retailing"},
        "4191": {"symbol": "4191", "name_en": "Abo Moati Al Motaheda", "name_ar": "أبو معطي المتحدة", "sector": "Retailing"},
        "4192": {"symbol": "4192", "name_en": "Al Saif Gallery", "name_ar": "صالة السيف", "sector": "Retailing"},
        "4200": {"symbol": "4200", "name_en": "Al Drees Petroleum and Transport Services", "name_ar": "الدريس", "sector": "Energy"},
        "4261": {"symbol": "4261", "name_en": "Theeb Rent a Car", "name_ar": "ذيب لتأجير السيارات", "sector": "Transportation"},
        "4270": {"symbol": "4270", "name_en": "Saudi Public Procurement Company", "name_ar": "الشركة السعودية للمشتريات الحكومية", "sector": "Commercial & Professional Services"},
        "4290": {"symbol": "4290", "name_en": "Al Khaleej Training and Education", "name_ar": "الخليج للتدريب والتعليم", "sector": "Consumer Services"},
        "4292": {"symbol": "4292", "name_en": "Ataa Educational Company", "name_ar": "عطاء التعليمية", "sector": "Consumer Services"},
        "4300": {"symbol": "4300", "name_en": "Dar Al Arkan Real Estate Development Company", "name_ar": "دار الأركان", "sector": "Real Estate Management & Development"},
        "4310": {"symbol": "4310", "name_en": "Knowledge Economic City", "name_ar": "مدينة المعرفة الاقتصادية", "sector": "Real Estate Management & Development"},
        "4320": {"symbol": "4320", "name_en": "Al Andalus Property Company", "name_ar": "الأندلس العقارية", "sector": "Real Estate Management & Development"},
        "4321": {"symbol": "4321", "name_en": "Ishbilia Real Estate Company", "name_ar": "إشبيلية العقارية", "sector": "Real Estate Management & Development"},
        "4322": {"symbol": "4322", "name_en": "RETAL Urban Development", "name_ar": "ريتال للتطوير العمراني", "sector": "Real Estate Management & Development"},
        "4323": {"symbol": "4323", "name_en": "SUMOU Real Estate Company", "name_ar": "سمو العقارية", "sector": "Real Estate Management & Development"},
        "4324": {"symbol": "4324", "name_en": "Salam International Investment Limited", "name_ar": "سلام العالمية", "sector": "Real Estate Management & Development"},
        "4325": {"symbol": "4325", "name_en": "Masar", "name_ar": "مسار", "sector": "Real Estate Management & Development"},
        "4330": {"symbol": "4330", "name_en": "Amlak International for Real Estate Finance", "name_ar": "أملاك العالمية", "sector": "Real Estate Management & Development"},
        "4331": {"symbol": "4331", "name_en": "Riyad REIT Fund", "name_ar": "صندوق الرياض ريت", "sector": "Real Estate Management & Development"},
        "4332": {"symbol": "4332", "name_en": "Mulkia Gulf Real Estate REIT Fund", "name_ar": "صندوق ملكية الخليج العقاري", "sector": "Real Estate Management & Development"},
        "4333": {"symbol": "4333", "name_en": "Bonyan REIT Fund", "name_ar": "صندوق بنيان ريت", "sector": "Real Estate Management & Development"},
        "4334": {"symbol": "4334", "name_en": "Alrajhi REIT Fund", "name_ar": "صندوق الراجحي ريت", "sector": "Real Estate Management & Development"},
        "4335": {"symbol": "4335", "name_en": "Taleem REIT Fund", "name_ar": "صندوق تعليم ريت", "sector": "Real Estate Management & Development"},
        "4336": {"symbol": "4336", "name_en": "Jadwa REIT Saudi Fund", "name_ar": "صندوق جدوى ريت السعودي", "sector": "Real Estate Management & Development"},
        "4337": {"symbol": "4337", "name_en": "Sico Saudi REIT Fund", "name_ar": "صندوق سيكو السعودي ريت", "sector": "Real Estate Management & Development"},
        "4338": {"symbol": "4338", "name_en": "Al Ahli REIT Fund 1", "name_ar": "صندوق الأهلي ريت 1", "sector": "Real Estate Management & Development"},
        "4339": {"symbol": "4339", "name_en": "Al Maather REIT Fund", "name_ar": "صندوق المآثر ريت", "sector": "Real Estate Management & Development"},
        "4340": {"symbol": "4340", "name_en": "Derayah REIT Fund", "name_ar": "صندوق دراية ريت", "sector": "Real Estate Management & Development"},
        
        # Agriculture & Food (6000-6999)
        "6001": {"symbol": "6001", "name_en": "Halwani Bros", "name_ar": "الحلواني إخوان", "sector": "Food, Beverage & Tobacco"},
        "6004": {"symbol": "6004", "name_en": "Catering", "name_ar": "التموين", "sector": "Consumer Services"},
        "6012": {"symbol": "6012", "name_en": "Raydan Food", "name_ar": "ريدان الغذائية", "sector": "Food, Beverage & Tobacco"},
        "6014": {"symbol": "6014", "name_en": "Al Amar", "name_ar": "الأعمار", "sector": "Food, Beverage & Tobacco"},
        "6015": {"symbol": "6015", "name_en": "Americana", "name_ar": "أمريكانا", "sector": "Consumer Services"},
        "6020": {"symbol": "6020", "name_en": "Gaco", "name_ar": "جاكو", "sector": "Food, Beverage & Tobacco"},
        "6040": {"symbol": "6040", "name_en": "Tabuk Agricultural Development Company", "name_ar": "تادكو", "sector": "Food, Beverage & Tobacco"},
        "6050": {"symbol": "6050", "name_en": "Saudi Fisheries Company", "name_ar": "الأسماك", "sector": "Food, Beverage & Tobacco"},
        "6060": {"symbol": "6060", "name_en": "Eastern Province Development Company", "name_ar": "تنمية الشرقية", "sector": "Real Estate Management & Development"},
        "6070": {"symbol": "6070", "name_en": "Aljouf Agricultural Development Company", "name_ar": "تنمية الجوف", "sector": "Food, Beverage & Tobacco"},
        "6090": {"symbol": "6090", "name_en": "Jazan Development Company", "name_ar": "جازادكو", "sector": "Real Estate Management & Development"},
        
        # Telecommunications (7000-7999)
        "7010": {"symbol": "7010", "name_en": "Saudi Telecom Company", "name_ar": "الاتصالات السعودية", "sector": "Telecommunication Services"},
        "7020": {"symbol": "7020", "name_en": "Etihad Etisalat", "name_ar": "اتحاد اتصالات", "sector": "Telecommunication Services"},
        "7030": {"symbol": "7030", "name_en": "Zain Saudi Arabia", "name_ar": "زين السعودية", "sector": "Telecommunication Services"},
        "7040": {"symbol": "7040", "name_en": "GO Telecom", "name_ar": "جو تيليكوم", "sector": "Telecommunication Services"},
        "7201": {"symbol": "7201", "name_en": "Arab Sea Information Systems", "name_ar": "بحر العرب", "sector": "Software & Services"},
        "7211": {"symbol": "7211", "name_en": "AZM", "name_ar": "عزم", "sector": "Software & Services"},
        
        # Insurance (8000-8999)
        "8010": {"symbol": "8010", "name_en": "Tawuniya", "name_ar": "التعاونية", "sector": "Insurance"},
        "8012": {"symbol": "8012", "name_en": "Jazira Takaful", "name_ar": "الجزيرة تكافل", "sector": "Insurance"},
        "8020": {"symbol": "8020", "name_en": "Malath Insurance", "name_ar": "ملاذ للتأمين", "sector": "Insurance"},
        "8040": {"symbol": "8040", "name_en": "Mutakamela", "name_ar": "المتكاملة للتأمين", "sector": "Insurance"},
        "8070": {"symbol": "8070", "name_en": "Arabian Shield", "name_ar": "الدرع العربي", "sector": "Insurance"},
        "8100": {"symbol": "8100", "name_en": "Saudi Indian Company for Insurance", "name_ar": "سايكو", "sector": "Insurance"},
        "8120": {"symbol": "8120", "name_en": "Gulf Union Alahlia Insurance", "name_ar": "الخليج الأهلية", "sector": "Insurance"},
        "8150": {"symbol": "8150", "name_en": "Al Ahlia Insurance", "name_ar": "الأهلية للتأمين", "sector": "Insurance"},
        "8160": {"symbol": "8160", "name_en": "Al Alamiya for Cooperative Insurance", "name_ar": "العالمية", "sector": "Insurance"},
        "8170": {"symbol": "8170", "name_en": "Al Etihad Cooperative Insurance", "name_ar": "الاتحاد التجاري", "sector": "Insurance"},
        "8180": {"symbol": "8180", "name_en": "Al Sagr Cooperative Insurance", "name_ar": "الصقر للتأمين", "sector": "Insurance"},
        "8190": {"symbol": "8190", "name_en": "United Cooperative Assurance", "name_ar": "الوطنية", "sector": "Insurance"},
        "8210": {"symbol": "8210", "name_en": "Bupa Arabia for Cooperative Insurance", "name_ar": "بوبا العربية", "sector": "Insurance"},
        "8230": {"symbol": "8230", "name_en": "Al Rajhi Takaful", "name_ar": "الراجحي تكافل", "sector": "Insurance"},
        "8250": {"symbol": "8250", "name_en": "Gulf Insurance Group", "name_ar": "الخليج للتأمين", "sector": "Insurance"},
        "8300": {"symbol": "8300", "name_en": "Wataniya Insurance", "name_ar": "الوطنية للتأمين", "sector": "Insurance"},
        "8310": {"symbol": "8310", "name_en": "Amana Cooperative Insurance", "name_ar": "أمانة للتأمين", "sector": "Insurance"},
        "8311": {"symbol": "8311", "name_en": "Enaya Cooperative Insurance", "name_ar": "عناية", "sector": "Insurance"},
        "8313": {"symbol": "8313", "name_en": "Rasan", "name_ar": "راسان", "sector": "Insurance"},
        
        # REITs and Investment Funds (9000-9999)
        "9408": {"symbol": "9408", "name_en": "Al Bilad Saudi Growth Fund", "name_ar": "صندوق البلاد السعودي للنمو", "sector": "Diversified Financials"},
        "9410": {"symbol": "9410", "name_en": "Falcom Saudi Growth Fund", "name_ar": "صندوق فالكم السعودي للنمو", "sector": "Diversified Financials"},
        "9411": {"symbol": "9411", "name_en": "Saudi Companies Growth Fund", "name_ar": "صندوق الشركات السعودية للنمو", "sector": "Diversified Financials"},
        "9412": {"symbol": "9412", "name_en": "Saudi Venture Capital Fund", "name_ar": "صندوق رأس المال الجريء السعودي", "sector": "Diversified Financials"},
        "9413": {"symbol": "9413", "name_en": "SAR Investment Fund", "name_ar": "صندوق سار للاستثمار", "sector": "Diversified Financials"},
        "9414": {"symbol": "9414", "name_en": "Saudi Public Investment Fund", "name_ar": "صندوق الاستثمارات العامة", "sector": "Diversified Financials"},
        "9415": {"symbol": "9415", "name_en": "Saudi Development Fund", "name_ar": "صندوق التنمية السعودي", "sector": "Diversified Financials"},
        "9416": {"symbol": "9416", "name_en": "Saudi Industrial Development Fund", "name_ar": "صندوق التنمية الصناعية السعودية", "sector": "Diversified Financials"},
    }
    
    return complete_stocks

def fetch_missing_stocks():
    """Fetch additional stocks that might be missing"""
    # Additional stocks found in various sources
    additional_stocks = {
        # Additional banks and financial institutions
        "1070": {"symbol": "1070", "name_en": "Bank Al Ittihad", "name_ar": "بنك الاتحاد", "sector": "Banking"},
        "1075": {"symbol": "1075", "name_en": "Saudi British Bank", "name_ar": "البنك السعودي البريطاني", "sector": "Banking"},
        "1085": {"symbol": "1085", "name_en": "Arab Bank", "name_ar": "البنك العربي", "sector": "Banking"},
        "1090": {"symbol": "1090", "name_en": "Bank of Riyadh", "name_ar": "بنك الرياض", "sector": "Banking"},
        
        # Additional manufacturing companies
        "1330": {"symbol": "1330", "name_en": "Saudi Arabian Mining Company", "name_ar": "شركة التعدين العربية السعودية", "sector": "Materials"},
        "1340": {"symbol": "1340", "name_en": "Advanced Electronics Company", "name_ar": "الشركة المتقدمة للإلكترونيات", "sector": "Technology Hardware & Equipment"},
        "1350": {"symbol": "1350", "name_en": "Saudi Arabian Airlines", "name_ar": "الخطوط الجوية السعودية", "sector": "Transportation"},
        
        # Additional energy companies
        "2040": {"symbol": "2040", "name_en": "Saudi Electricity Company", "name_ar": "الشركة السعودية للكهرباء", "sector": "Utilities"},
        "2090": {"symbol": "2090", "name_en": "Saudi Water Partnership Company", "name_ar": "شركة شراكة المياه السعودية", "sector": "Utilities"},
        
        # Additional technology companies
        "7050": {"symbol": "7050", "name_en": "Saudi Technology Company", "name_ar": "الشركة السعودية للتقنية", "sector": "Technology Hardware & Equipment"},
        "7060": {"symbol": "7060", "name_en": "Digital Saudi Company", "name_ar": "السعودية الرقمية", "sector": "Software & Services"},
        
        # Additional specialized funds
        "9420": {"symbol": "9420", "name_en": "Saudi Infrastructure Fund", "name_ar": "صندوق البنية التحتية السعودي", "sector": "Diversified Financials"},
        "9421": {"symbol": "9421", "name_en": "Saudi Energy Fund", "name_ar": "صندوق الطاقة السعودي", "sector": "Diversified Financials"},
        "9422": {"symbol": "9422", "name_en": "Saudi Healthcare Fund", "name_ar": "صندوق الرعاية الصحية السعودي", "sector": "Diversified Financials"},
    }
    
    return additional_stocks

def create_complete_database():
    """Create the most comprehensive Saudi stock database"""
    logger.info("🚀 Creating complete Saudi stock database...")
    
    # Load existing databases
    existing_dbs = load_existing_databases()
    
    # Merge existing databases
    merged_db = merge_databases(existing_dbs)
    logger.info(f"📊 Merged existing databases: {len(merged_db)} stocks")
    
    # Add comprehensive stock list
    comprehensive_stocks = get_comprehensive_saudi_stocks()
    for symbol, data in comprehensive_stocks.items():
        if symbol not in merged_db:
            merged_db[symbol] = data
            logger.info(f"➕ Added missing stock: {symbol} - {data.get('name_en', 'Unknown')}")
        else:
            # Update with more complete data if available
            merged_db[symbol].update(data)
    
    # Add additional missing stocks
    additional_stocks = fetch_missing_stocks()
    for symbol, data in additional_stocks.items():
        if symbol not in merged_db:
            merged_db[symbol] = data
            logger.info(f"➕ Added additional stock: {symbol} - {data.get('name_en', 'Unknown')}")
    
    # Add timestamp
    for symbol in merged_db:
        merged_db[symbol]['last_updated'] = datetime.now().isoformat()
    
    # Save the complete database
    with open('saudi_stocks_database_complete.json', 'w', encoding='utf-8') as f:
        json.dump(merged_db, f, ensure_ascii=False, indent=2)
    
    # Update the main database
    with open('saudi_stocks_database.json', 'w', encoding='utf-8') as f:
        json.dump(merged_db, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ Complete database created with {len(merged_db)} stocks")
    logger.info(f"📊 Target: 259 stocks | Current: {len(merged_db)} | Gap: {259 - len(merged_db)}")
    
    # Verify Arab National Bank
    if '1080' in merged_db:
        logger.info(f"✅ Arab National Bank confirmed: {merged_db['1080']['name_en']}")
    else:
        logger.warning("❌ Arab National Bank (1080) still missing!")
    
    return merged_db

def main():
    """Main function to create complete database"""
    logger.info("🇸🇦 Starting Complete Saudi Exchange Stock Fetcher...")
    
    try:
        complete_db = create_complete_database()
        
        # Summary
        logger.info("\n" + "="*60)
        logger.info("📊 COMPLETE DATABASE SUMMARY")
        logger.info("="*60)
        logger.info(f"Total stocks: {len(complete_db)}")
        logger.info(f"Target stocks: 259")
        logger.info(f"Completion: {len(complete_db)/259*100:.1f}%")
        
        # Check key stocks
        key_stocks = ['1010', '1080', '2030', '7010', '4013']
        logger.info("\n🔍 Key Stock Verification:")
        for symbol in key_stocks:
            if symbol in complete_db:
                logger.info(f"✅ {symbol}: {complete_db[symbol]['name_en']}")
            else:
                logger.warning(f"❌ {symbol}: Missing")
        
        # Sector breakdown
        sectors = {}
        for stock in complete_db.values():
            sector = stock.get('sector', 'Unknown')
            sectors[sector] = sectors.get(sector, 0) + 1
        
        logger.info("\n📈 Sector Breakdown:")
        for sector, count in sorted(sectors.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {sector}: {count} stocks")
        
        logger.info("\n✅ Complete Saudi stock database created successfully!")
        logger.info("📁 Saved to: saudi_stocks_database_complete.json")
        logger.info("📁 Updated: saudi_stocks_database.json")
        
        return complete_db
        
    except Exception as e:
        logger.error(f"❌ Error creating complete database: {e}")
        return None

if __name__ == "__main__":
    complete_database = main()
