"""
🇸🇦 Saudi Stock Exchange (Tadawul) Stock Database
Comprehensive database of all Saudi stocks with symbols, names, and sectors
"""

import json
import requests
import pandas as pd
from datetime import datetime
import yfinance as yf
import time

class SaudiStockDatabase:
    """Saudi Stock Exchange Database Manager"""
    
    def __init__(self):
        self.stocks_data = {}
        self.last_updated = None
    
    def get_saudi_stocks_from_yfinance(self):
        """Get Saudi stocks data from yfinance and manual database"""
        
        # Known major Saudi stocks with their information
        saudi_stocks = {
            "1010": {
                "symbol": "1010.SR",
                "name_en": "Saudi National Bank",
                "name_ar": "البنك الأهلي السعودي",
                "sector": "Banking",
                "industry": "Financial Services",
                "market_cap": "Large Cap"
            },
            "1020": {
                "symbol": "1020.SR", 
                "name_en": "Bank AlJazira",
                "name_ar": "بنك الجزيرة",
                "sector": "Banking",
                "industry": "Financial Services", 
                "market_cap": "Mid Cap"
            },
            "1030": {
                "symbol": "1030.SR",
                "name_en": "Alinma Bank", 
                "name_ar": "بنك الإنماء",
                "sector": "Banking",
                "industry": "Financial Services",
                "market_cap": "Mid Cap"
            },
            "1050": {
                "symbol": "1050.SR",
                "name_en": "Bank Albilad",
                "name_ar": "بنك البلاد", 
                "sector": "Banking",
                "industry": "Financial Services",
                "market_cap": "Mid Cap"
            },
            "1060": {
                "symbol": "1060.SR",
                "name_en": "Saudi Investment Bank",
                "name_ar": "البنك السعودي للاستثمار",
                "sector": "Banking", 
                "industry": "Financial Services",
                "market_cap": "Mid Cap"
            },
            "1080": {
                "symbol": "1080.SR",
                "name_en": "Arab National Bank",
                "name_ar": "البنك العربي الوطني",
                "sector": "Banking",
                "industry": "Financial Services",
                "market_cap": "Mid Cap"
            },
            "1120": {
                "symbol": "1120.SR",
                "name_en": "Al Rajhi Bank",
                "name_ar": "مصرف الراجحي",
                "sector": "Banking",
                "industry": "Financial Services", 
                "market_cap": "Large Cap"
            },
            "1140": {
                "symbol": "1140.SR",
                "name_en": "Bank AlBilad",
                "name_ar": "بنك البلاد",
                "sector": "Banking",
                "industry": "Financial Services",
                "market_cap": "Mid Cap"
            },
            "1150": {
                "symbol": "1150.SR",
                "name_en": "Banque Saudi Fransi",
                "name_ar": "البنك السعودي الفرنسي",
                "sector": "Banking",
                "industry": "Financial Services",
                "market_cap": "Mid Cap"
            },
            "1180": {
                "symbol": "1180.SR",
                "name_en": "National Medical Care",
                "name_ar": "الرعاية الطبية الوطنية",
                "sector": "Healthcare",
                "industry": "Healthcare Services",
                "market_cap": "Mid Cap"
            },
            "1182": {
                "symbol": "1182.SR",
                "name_en": "Elm Company",
                "name_ar": "شركة علم",
                "sector": "Technology",
                "industry": "IT Services",
                "market_cap": "Mid Cap"
            },
            "1201": {
                "symbol": "1201.SR",
                "name_en": "Tashelat Marketing",
                "name_ar": "تسهيلات للتسويق",
                "sector": "Consumer Services",
                "industry": "Marketing Services",
                "market_cap": "Small Cap"
            },
            "1210": {
                "symbol": "1210.SR",
                "name_en": "BinDawood Holding",
                "name_ar": "مجموعة بن داود القابضة",
                "sector": "Consumer Staples",
                "industry": "Retail",
                "market_cap": "Mid Cap"
            },
            "1301": {
                "symbol": "1301.SR",
                "name_en": "Alouja Development",
                "name_ar": "العوجا للتنمية",
                "sector": "Real Estate",
                "industry": "Real Estate Development",
                "market_cap": "Small Cap"
            },
            "1320": {
                "symbol": "1320.SR",
                "name_en": "Saudi Fisheries",
                "name_ar": "الأسماك السعودية",
                "sector": "Consumer Staples",
                "industry": "Food Production",
                "market_cap": "Small Cap"
            },
            "2010": {
                "symbol": "2010.SR",
                "name_en": "Saudi Basic Industries Corp",
                "name_ar": "سابك",
                "sector": "Materials",
                "industry": "Chemicals",
                "market_cap": "Large Cap"
            },
            "2020": {
                "symbol": "2020.SR",
                "name_en": "Saudi Cement",
                "name_ar": "الأسمنت السعودية",
                "sector": "Materials",
                "industry": "Construction Materials",
                "market_cap": "Mid Cap"
            },
            "2030": {
                "symbol": "2030.SR",
                "name_en": "Saudi Arabian Oil Co",
                "name_ar": "أرامكو السعودية",
                "sector": "Energy",
                "industry": "Oil & Gas",
                "market_cap": "Large Cap"
            },
            "2040": {
                "symbol": "2040.SR",
                "name_en": "Saudi Electricity",
                "name_ar": "الكهرباء السعودية",
                "sector": "Utilities",
                "industry": "Electric Utilities",
                "market_cap": "Large Cap"
            },
            "2050": {
                "symbol": "2050.SR",
                "name_en": "Jarir Marketing",
                "name_ar": "جرير للتسويق",
                "sector": "Consumer Discretionary",
                "industry": "Retail",
                "market_cap": "Mid Cap"
            },
            "2060": {
                "symbol": "2060.SR",
                "name_en": "Saudi Telecom",
                "name_ar": "الاتصالات السعودية",
                "sector": "Communication Services",
                "industry": "Telecommunications",
                "market_cap": "Large Cap"
            },
            "2080": {
                "symbol": "2080.SR",
                "name_en": "Saudi Arabian Mining",
                "name_ar": "معادن",
                "sector": "Materials",
                "industry": "Mining",
                "market_cap": "Large Cap"
            },
            "2090": {
                "symbol": "2090.SR",
                "name_en": "Saudi Industrial Export",
                "name_ar": "الصادرات الصناعية",
                "sector": "Industrials",
                "industry": "Industrial Services",
                "market_cap": "Small Cap"
            },
            "2100": {
                "symbol": "2100.SR",
                "name_en": "Wafrah for Industry and Development",
                "name_ar": "وفرة للصناعة والتنمية",
                "sector": "Industrials",
                "industry": "Industrial Development",
                "market_cap": "Small Cap"
            },
            "2110": {
                "symbol": "2110.SR",
                "name_en": "Eastern Province Cement",
                "name_ar": "أسمنت المنطقة الشرقية",
                "sector": "Materials",
                "industry": "Construction Materials",
                "market_cap": "Mid Cap"
            },
            "2120": {
                "symbol": "2120.SR",
                "name_en": "Saudi Ceramic",
                "name_ar": "السيراميك السعودي",
                "sector": "Materials",
                "industry": "Construction Materials",
                "market_cap": "Small Cap"
            },
            "2130": {
                "symbol": "2130.SR",
                "name_en": "Saudi Arabian Fertilizer",
                "name_ar": "سافكو",
                "sector": "Materials",
                "industry": "Chemicals",
                "market_cap": "Mid Cap"
            },
            "2140": {
                "symbol": "2140.SR",
                "name_en": "Red Sea International",
                "name_ar": "البحر الأحمر الدولية",
                "sector": "Consumer Discretionary", 
                "industry": "Tourism & Entertainment",
                "market_cap": "Large Cap"
            },
            "2150": {
                "symbol": "2150.SR",
                "name_en": "Pharmaceutical Solutions Industry",
                "name_ar": "صناعة الحلول الدوائية",
                "sector": "Healthcare",
                "industry": "Pharmaceuticals",
                "market_cap": "Small Cap"
            },
            "2160": {
                "symbol": "2160.SR",
                "name_en": "Saudi Arabian Amiantit",
                "name_ar": "أميانتيت السعودية",
                "sector": "Materials",
                "industry": "Construction Materials",
                "market_cap": "Small Cap"
            },
            "2170": {
                "symbol": "2170.SR",
                "name_en": "Almarai",
                "name_ar": "المراعي",
                "sector": "Consumer Staples",
                "industry": "Food & Beverages",
                "market_cap": "Large Cap"
            },
            "2180": {
                "symbol": "2180.SR",
                "name_en": "Fitaihi Holding Group",
                "name_ar": "مجموعة فتيحي القابضة",
                "sector": "Consumer Discretionary",
                "industry": "Retail",
                "market_cap": "Small Cap"
            },
            "2190": {
                "symbol": "2190.SR",
                "name_en": "Saudi Automotive Services",
                "name_ar": "الخدمات السيارة السعودية",
                "sector": "Consumer Discretionary",
                "industry": "Automotive Services",
                "market_cap": "Small Cap"
            },
            "2200": {
                "symbol": "2200.SR",
                "name_en": "Anaam International Holding",
                "name_ar": "أنعام القابضة الدولية",
                "sector": "Consumer Staples",
                "industry": "Food Production",
                "market_cap": "Small Cap"
            },
            "2210": {
                "symbol": "2210.SR",
                "name_en": "Nama Chemicals",
                "name_ar": "نماء للكيماويات",
                "sector": "Materials",
                "industry": "Chemicals",
                "market_cap": "Mid Cap"
            },
            "2220": {
                "symbol": "2220.SR",
                "name_en": "Saudi Cement",
                "name_ar": "الأسمنت السعودية",
                "sector": "Materials",
                "industry": "Construction Materials",
                "market_cap": "Mid Cap"
            },
            "2230": {
                "symbol": "2230.SR",
                "name_en": "Yanbu Cement",
                "name_ar": "أسمنت ينبع",
                "sector": "Materials",
                "industry": "Construction Materials",
                "market_cap": "Small Cap"
            },
            "2240": {
                "symbol": "2240.SR",
                "name_en": "Zamil Industrial Investment",
                "name_ar": "الزامل للاستثمار الصناعي",
                "sector": "Industrials",
                "industry": "Industrial Equipment",
                "market_cap": "Mid Cap"
            },
            "2250": {
                "symbol": "2250.SR",
                "name_en": "Saudi Industrial Development Fund",
                "name_ar": "صندوق التنمية الصناعية السعودي",
                "sector": "Financials",
                "industry": "Development Funds",
                "market_cap": "Mid Cap"
            },
            "2260": {
                "symbol": "2260.SR",
                "name_en": "Saudi Paper Manufacturing",
                "name_ar": "السعودية لصناعة الورق",
                "sector": "Materials",
                "industry": "Paper & Packaging",
                "market_cap": "Small Cap"
            },
            "2270": {
                "symbol": "2270.SR",
                "name_en": "Saudi Arabian Oil Pipes",
                "name_ar": "أنابيب النفط السعودية",
                "sector": "Energy",
                "industry": "Oil Equipment & Services",
                "market_cap": "Small Cap"
            },
            "2280": {
                "symbol": "2280.SR",
                "name_en": "Saudi Arabian Mining (Ma'aden)",
                "name_ar": "معادن",
                "sector": "Materials",
                "industry": "Mining",
                "market_cap": "Large Cap"
            },
            "2290": {
                "symbol": "2290.SR",
                "name_en": "Yanbu National Petrochemical",
                "name_ar": "ينبع الوطنية للبتروكيماويات",
                "sector": "Materials",
                "industry": "Chemicals",
                "market_cap": "Mid Cap"
            },
            "2300": {
                "symbol": "2300.SR",
                "name_en": "Saudi Industrial Services",
                "name_ar": "الخدمات الصناعية السعودية",
                "sector": "Industrials",
                "industry": "Industrial Services",
                "market_cap": "Small Cap"
            },
            "2310": {
                "symbol": "2310.SR",
                "name_en": "Sipchem",
                "name_ar": "سبكيم",
                "sector": "Materials",
                "industry": "Chemicals",
                "market_cap": "Mid Cap"
            },
            "2320": {
                "symbol": "2320.SR",
                "name_en": "Saudi Arabia Refineries",
                "name_ar": "مصافي أرامكو السعودية",
                "sector": "Energy",
                "industry": "Oil Refining",
                "market_cap": "Large Cap"
            },
            "2330": {
                "symbol": "2330.SR",
                "name_en": "Advanced Petrochemical",
                "name_ar": "المتقدمة للبتروكيماويات",
                "sector": "Materials",
                "industry": "Chemicals",
                "market_cap": "Mid Cap"
            },
            "2340": {
                "symbol": "2340.SR",
                "name_en": "Saudi Kayan Petrochemical",
                "name_ar": "كيان السعودية للبتروكيماويات",
                "sector": "Materials",
                "industry": "Chemicals",
                "market_cap": "Mid Cap"
            },
            "2350": {
                "symbol": "2350.SR",
                "name_en": "Saudi Chemical",
                "name_ar": "الكيميائية السعودية",
                "sector": "Materials",
                "industry": "Chemicals",
                "market_cap": "Small Cap"
            },
            "2360": {
                "symbol": "2360.SR",
                "name_en": "Saudi International Petrochemical",
                "name_ar": "سبكيم العالمية",
                "sector": "Materials",
                "industry": "Chemicals",
                "market_cap": "Mid Cap"
            },
            "2370": {
                "symbol": "2370.SR",
                "name_en": "Saudi Arabia Oil Company",
                "name_ar": "شركة النفط السعودية",
                "sector": "Energy",
                "industry": "Oil & Gas",
                "market_cap": "Large Cap"
            },
            "2380": {
                "symbol": "2380.SR",
                "name_en": "Saudi Electricity Company",
                "name_ar": "الشركة السعودية للكهرباء",
                "sector": "Utilities",
                "industry": "Electric Utilities",
                "market_cap": "Large Cap"
            },
            "2390": {
                "symbol": "2390.SR",
                "name_en": "Saudi Arabian Public Transport",
                "name_ar": "النقل العام السعودي",
                "sector": "Industrials",
                "industry": "Transportation",
                "market_cap": "Small Cap"
            },
            "4001": {
                "symbol": "4001.SR",
                "name_en": "Dallah Healthcare",
                "name_ar": "دله للخدمات الصحية",
                "sector": "Healthcare",
                "industry": "Healthcare Services",
                "market_cap": "Mid Cap"
            },
            "4002": {
                "symbol": "4002.SR",
                "name_en": "Mouwasat Medical Services",
                "name_ar": "المواساة للخدمات الطبية",
                "sector": "Healthcare",
                "industry": "Healthcare Services",
                "market_cap": "Mid Cap"
            },
            "4003": {
                "symbol": "4003.SR",
                "name_en": "Saudi Pharmaceutical Industries",
                "name_ar": "الصناعات الدوائية السعودية",
                "sector": "Healthcare",
                "industry": "Pharmaceuticals",
                "market_cap": "Small Cap"
            },
            "4004": {
                "symbol": "4004.SR",
                "name_en": "Dr. Sulaiman Al Habib Medical Services",
                "name_ar": "د. سليمان الحبيب للخدمات الطبية",
                "sector": "Healthcare",
                "industry": "Healthcare Services",
                "market_cap": "Large Cap"
            },
            "4005": {
                "symbol": "4005.SR",
                "name_en": "Saudi Enaya Cooperative Insurance",
                "name_ar": "عناية السعودية للتأمين التعاوني",
                "sector": "Financials",
                "industry": "Insurance",
                "market_cap": "Small Cap"
            },
            "4030": {
                "symbol": "4030.SR",
                "name_en": "United Electronics Company",
                "name_ar": "شركة الإلكترونيات المتحدة",
                "sector": "Consumer Discretionary",
                "industry": "Electronics Retail",
                "market_cap": "Mid Cap"
            },
            "4031": {
                "symbol": "4031.SR",
                "name_en": "Gulf General Cooperative Insurance",
                "name_ar": "الخليج العامة للتأمين التعاوني",
                "sector": "Financials",
                "industry": "Insurance",
                "market_cap": "Small Cap"
            },
            "4040": {
                "symbol": "4040.SR",
                "name_en": "Saudi Research and Media Group",
                "name_ar": "مجموعة السعودية للأبحاث والإعلام",
                "sector": "Communication Services",
                "industry": "Media",
                "market_cap": "Mid Cap"
            },
            "4050": {
                "symbol": "4050.SR",
                "name_en": "Saudi Airlines Catering",
                "name_ar": "الخطوط السعودية للتموين",
                "sector": "Consumer Discretionary",
                "industry": "Airlines",
                "market_cap": "Small Cap"
            },
            "4061": {
                "symbol": "4061.SR",
                "name_en": "Abdullah Al Othaim Markets",
                "name_ar": "أسواق عبدالله العثيم",
                "sector": "Consumer Staples",
                "industry": "Retail",
                "market_cap": "Mid Cap"
            },
            "4070": {
                "symbol": "4070.SR",
                "name_en": "Tihama Advertising and Public Relations",
                "name_ar": "تهامة للإعلان والعلاقات العامة",
                "sector": "Communication Services",
                "industry": "Advertising",
                "market_cap": "Small Cap"
            },
            "4080": {
                "symbol": "4080.SR",
                "name_en": "Saudi Automotive Services",
                "name_ar": "الخدمات السيارة السعودية",
                "sector": "Consumer Discretionary",
                "industry": "Automotive Services",
                "market_cap": "Small Cap"
            },
            "4090": {
                "symbol": "4090.SR",
                "name_en": "Tamweel Al Oula",
                "name_ar": "تمويل الأولى",
                "sector": "Financials",
                "industry": "Financial Services",
                "market_cap": "Small Cap"
            },
            "4100": {
                "symbol": "4100.SR",
                "name_en": "Maharah Human Resources",
                "name_ar": "مهارة للموارد البشرية",
                "sector": "Industrials",
                "industry": "Human Resources",
                "market_cap": "Small Cap"
            },
            "4110": {
                "symbol": "4110.SR",
                "name_en": "Dur Hospitality",
                "name_ar": "در للضيافة",
                "sector": "Consumer Discretionary",
                "industry": "Hotels & Hospitality",
                "market_cap": "Small Cap"
            },
            "4150": {
                "symbol": "4150.SR",
                "name_en": "Andalusia Health",
                "name_ar": "الأندلس للصحة",
                "sector": "Healthcare",
                "industry": "Healthcare Services",
                "market_cap": "Small Cap"
            },
            "4160": {
                "symbol": "4160.SR",
                "name_en": "Saudi Technology Development and Investment",
                "name_ar": "التطوير والاستثمار التقني السعودي",
                "sector": "Technology",
                "industry": "Technology Investment",
                "market_cap": "Small Cap"
            },
            "4170": {
                "symbol": "4170.SR",
                "name_en": "Miahona",
                "name_ar": "مياهنا",
                "sector": "Utilities",
                "industry": "Water Utilities",
                "market_cap": "Small Cap"
            },
            "4180": {
                "symbol": "4180.SR",
                "name_en": "Saudi Company for Hardware",
                "name_ar": "السعودية للأجهزة",
                "sector": "Consumer Discretionary",
                "industry": "Hardware Retail",
                "market_cap": "Small Cap"
            },
            "4190": {
                "symbol": "4190.SR",
                "name_en": "Jabal Omar Development",
                "name_ar": "جبل عمر للتطوير",
                "sector": "Real Estate",
                "industry": "Real Estate Development",
                "market_cap": "Mid Cap"
            },
            "4200": {
                "symbol": "4200.SR",
                "name_en": "Al Hammadi Company for Development and Investment",
                "name_ar": "الحمادي للتنمية والاستثمار",
                "sector": "Real Estate",
                "industry": "Real Estate Development",
                "market_cap": "Small Cap"
            },
            "4210": {
                "symbol": "4210.SR",
                "name_en": "Al Baha Investment and Development",
                "name_ar": "الباحة للاستثمار والتنمية",
                "sector": "Real Estate",
                "industry": "Real Estate Development",
                "market_cap": "Small Cap"
            },
            "4220": {
                "symbol": "4220.SR",
                "name_en": "Saudi Ground Services",
                "name_ar": "الخدمات الأرضية السعودية",
                "sector": "Industrials",
                "industry": "Airport Services",
                "market_cap": "Small Cap"
            },
            "4230": {
                "symbol": "4230.SR",
                "name_en": "Saudi Company for Hardware",
                "name_ar": "السعودية للأجهزة",
                "sector": "Consumer Discretionary",
                "industry": "Hardware Retail",
                "market_cap": "Small Cap"
            },
            "4240": {
                "symbol": "4240.SR",
                "name_en": "Saudi Pharmaceutical Manufacturing",
                "name_ar": "التصنيع الدوائي السعودي",
                "sector": "Healthcare",
                "industry": "Pharmaceuticals",
                "market_cap": "Small Cap"
            },
            "4250": {
                "symbol": "4250.SR",
                "name_en": "Saudi Arabian Cooperative Insurance",
                "name_ar": "السعودية للتأمين التعاوني",
                "sector": "Financials",
                "industry": "Insurance",
                "market_cap": "Small Cap"
            },
            "4260": {
                "symbol": "4260.SR",
                "name_en": "Saudi Industrial Investment Group",
                "name_ar": "مجموعة الاستثمار الصناعي السعودي",
                "sector": "Industrials",
                "industry": "Industrial Investment",
                "market_cap": "Mid Cap"
            },
            "4270": {
                "symbol": "4270.SR",
                "name_en": "Saudi Cable Company",
                "name_ar": "الكابلات السعودية",
                "sector": "Industrials",
                "industry": "Electrical Equipment",
                "market_cap": "Small Cap"
            },
            "4280": {
                "symbol": "4280.SR",
                "name_en": "Arabian Centres",
                "name_ar": "المراكز العربية",
                "sector": "Real Estate",
                "industry": "Real Estate Services",
                "market_cap": "Large Cap"
            },
            "4290": {
                "symbol": "4290.SR",
                "name_en": "Kunooz Real Estate",
                "name_ar": "كنوز العقارية",
                "sector": "Real Estate",
                "industry": "Real Estate Development",
                "market_cap": "Small Cap"
            },
            "4300": {
                "symbol": "4300.SR",
                "name_en": "Saudi Company for Pharmaceutical Industries",
                "name_ar": "السعودية للصناعات الدوائية",
                "sector": "Healthcare",
                "industry": "Pharmaceuticals",
                "market_cap": "Small Cap"
            },
            "4310": {
                "symbol": "4310.SR",
                "name_en": "United Electronics Company",
                "name_ar": "شركة الإلكترونيات المتحدة",
                "sector": "Consumer Discretionary",
                "industry": "Electronics Retail",
                "market_cap": "Mid Cap"
            },
            "4320": {
                "symbol": "4320.SR",
                "name_en": "Saudi Airlines Catering",
                "name_ar": "الخطوط السعودية للتموين",
                "sector": "Consumer Discretionary",
                "industry": "Airlines",
                "market_cap": "Small Cap"
            },
            "4330": {
                "symbol": "4330.SR",
                "name_en": "Saudi Transport and Logistics",
                "name_ar": "النقل واللوجستيات السعودية",
                "sector": "Industrials",
                "industry": "Transportation",
                "market_cap": "Small Cap"
            },
            "4340": {
                "symbol": "4340.SR",
                "name_en": "Saudi Automotive Services",
                "name_ar": "الخدمات السيارة السعودية",
                "sector": "Consumer Discretionary",
                "industry": "Automotive Services",
                "market_cap": "Small Cap"
            },
            "4350": {
                "symbol": "4350.SR",
                "name_en": "Saudi Airlines Ground Services",
                "name_ar": "الخدمات الأرضية السعودية",
                "sector": "Industrials",
                "industry": "Airport Services",
                "market_cap": "Small Cap"
            },
            "7010": {
                "symbol": "7010.SR",
                "name_en": "Saudi Arabian Oil Company (Aramco)",
                "name_ar": "أرامكو السعودية",
                "sector": "Energy",
                "industry": "Oil & Gas",
                "market_cap": "Large Cap"
            }
        }
        
        return saudi_stocks
    
    def validate_and_enhance_stocks(self, stocks_dict):
        """Validate and enhance stock data with real-time information"""
        
        validated_stocks = {}
        
        for symbol, data in stocks_dict.items():
            try:
                # Try to get real price data to validate
                ticker = yf.Ticker(data['symbol'])
                info = ticker.history(period="1d")
                
                if not info.empty:
                    # Stock exists and has data
                    current_price = info['Close'].iloc[-1] if len(info) > 0 else None
                    
                    validated_stocks[symbol] = {
                        **data,
                        'last_price': current_price,
                        'status': 'active',
                        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    print(f"✅ Validated: {symbol} - {data['name_en']}")
                else:
                    # Add anyway but mark as unverified
                    validated_stocks[symbol] = {
                        **data,
                        'last_price': None,
                        'status': 'unverified',
                        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    print(f"⚠️ Unverified: {symbol} - {data['name_en']}")
                
                # Add small delay to avoid rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                # Add anyway but mark as error
                validated_stocks[symbol] = {
                    **data,
                    'last_price': None,
                    'status': 'error',
                    'error': str(e),
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                print(f"❌ Error: {symbol} - {str(e)}")
        
        return validated_stocks
    
    def save_to_json(self, stocks_data, filename="saudi_stocks_database.json"):
        """Save stocks data to JSON file"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stocks_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved {len(stocks_data)} stocks to {filename}")
    
    def load_from_json(self, filename="saudi_stocks_database.json"):
        """Load stocks data from JSON file"""
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                stocks_data = json.load(f)
            
            print(f"📖 Loaded {len(stocks_data)} stocks from {filename}")
            return stocks_data
        
        except FileNotFoundError:
            print(f"❌ File {filename} not found")
            return {}
        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")
            return {}
    
    def search_stocks(self, query, stocks_data):
        """Search stocks by symbol, name, or sector"""
        
        query = query.lower()
        results = []
        
        for symbol, data in stocks_data.items():
            if (query in symbol.lower() or 
                query in data['name_en'].lower() or 
                query in data.get('name_ar', '').lower() or
                query in data['sector'].lower()):
                
                results.append({
                    'symbol': symbol,
                    'symbol_full': data['symbol'],
                    'name_en': data['name_en'],
                    'name_ar': data.get('name_ar', ''),
                    'sector': data['sector'],
                    'market_cap': data.get('market_cap', 'Unknown'),
                    'last_price': data.get('last_price'),
                    'status': data.get('status', 'unknown')
                })
        
        return results
    
    def get_stocks_by_sector(self, stocks_data):
        """Group stocks by sector"""
        
        sectors = {}
        
        for symbol, data in stocks_data.items():
            sector = data['sector']
            if sector not in sectors:
                sectors[sector] = []
            
            sectors[sector].append({
                'symbol': symbol,
                'symbol_full': data['symbol'],
                'name_en': data['name_en'],
                'market_cap': data.get('market_cap', 'Unknown'),
                'last_price': data.get('last_price'),
                'status': data.get('status', 'unknown')
            })
        
        # Sort sectors and stocks within each sector
        sorted_sectors = {}
        for sector in sorted(sectors.keys()):
            sorted_sectors[sector] = sorted(sectors[sector], key=lambda x: x['symbol'])
        
        return sorted_sectors
    
    def create_database(self):
        """Create complete Saudi stocks database"""
        
        print("🚀 Creating Saudi Stock Exchange Database...")
        
        # Get stocks data
        stocks_data = self.get_saudi_stocks_from_yfinance()
        print(f"📊 Found {len(stocks_data)} Saudi stocks")
        
        # Validate and enhance with real-time data
        print("🔍 Validating stocks with real-time data...")
        validated_stocks = self.validate_and_enhance_stocks(stocks_data)
        
        # Save to JSON
        self.save_to_json(validated_stocks)
        
        # Create summary
        active_count = len([s for s in validated_stocks.values() if s.get('status') == 'active'])
        sectors = set(s['sector'] for s in validated_stocks.values())
        
        print(f"\n✅ Database created successfully!")
        print(f"📊 Total stocks: {len(validated_stocks)}")
        print(f"✅ Active stocks: {active_count}")
        print(f"📈 Sectors: {len(sectors)}")
        print(f"🏛️ Main sectors: {', '.join(sorted(sectors))}")
        
        return validated_stocks

def main():
    """Main function to create Saudi stocks database"""
    
    print("🇸🇦 Saudi Stock Exchange Database Creator")
    print("=" * 50)
    
    db = SaudiStockDatabase()
    
    # Create the database
    stocks_data = db.create_database()
    
    # Show some examples
    print("\n📋 Sample stocks by sector:")
    sectors = db.get_stocks_by_sector(stocks_data)
    
    for sector, stocks in list(sectors.items())[:5]:  # Show first 5 sectors
        print(f"\n{sector}:")
        for stock in stocks[:3]:  # Show first 3 stocks per sector
            status_emoji = "✅" if stock['status'] == 'active' else "⚠️"
            price_info = f"@ {stock['last_price']:.2f} SAR" if stock['last_price'] else "Price N/A"
            print(f"  {status_emoji} {stock['symbol']} - {stock['name_en']} {price_info}")
    
    print(f"\n💾 Database saved as 'saudi_stocks_database.json'")
    print("🎯 You can now use this database in your portfolio manager!")

if __name__ == "__main__":
    main()
