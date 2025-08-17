import json

# Load the database
with open('saudi_stocks_database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

print(f"📊 Database Analysis:")
print(f"  Total stocks: {len(db)}")
print(f"  Expected: 259")
print(f"  Missing: {259 - len(db)} stocks")

# Search for Arab National Bank
anb_found = []
for symbol, data in db.items():
    name = data.get('name_en', '').lower()
    if 'arab' in name and 'national' in name:
        anb_found.append(f"{symbol}: {data.get('name_en', '')}")

print(f"\n🏦 Arab National Bank search:")
if anb_found:
    for bank in anb_found:
        print(f"  ✅ {bank}")
else:
    print("  ❌ Arab National Bank not found")

# Check for missing 1080 symbol (mentioned in portfolio files)
if '1080' in db:
    print(f"\n✅ Symbol 1080: {db['1080']['name_en']}")
else:
    print(f"\n❌ Symbol 1080 missing from database")

# Show Arab-related banks
arab_banks = []
for symbol, data in db.items():
    name = data.get('name_en', '').lower()
    if 'arab' in name:
        arab_banks.append(f"{symbol}: {data.get('name_en', '')}")

print(f"\n🔍 All Arab-related banks ({len(arab_banks)}):")
for bank in arab_banks[:5]:  # Show first 5
    print(f"  {bank}")
if len(arab_banks) > 5:
    print(f"  ... and {len(arab_banks) - 5} more")
