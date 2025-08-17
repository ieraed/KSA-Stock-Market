#!/usr/bin/env python3
import json
from datetime import datetime

def upgrade_portfolio():
    """Add broker and notes fields to existing portfolio entries"""
    try:
        # Load existing portfolio
        with open('user_portfolio.json', 'r', encoding='utf-8') as f:
            portfolio = json.load(f)
        
        print(f"📊 Upgrading portfolio with {len(portfolio)} stocks...")
        
        # Add missing fields to existing entries
        updated_count = 0
        for stock in portfolio:
            if 'broker' not in stock:
                stock['broker'] = 'Not Set'
                updated_count += 1
            
            if 'notes' not in stock:
                stock['notes'] = ''
                updated_count += 1
        
        # Save upgraded portfolio
        with open('user_portfolio.json', 'w', encoding='utf-8') as f:
            json.dump(portfolio, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Portfolio upgraded successfully!")
        print(f"📈 Updated {updated_count} entries with broker and notes fields")
        
        # Display current portfolio with new fields
        print("\n📋 Current Portfolio:")
        for stock in portfolio:
            print(f"  {stock['symbol']}: {stock['quantity']:,} shares @ {stock['purchase_price']:.2f} SAR")
            print(f"    Broker: {stock.get('broker', 'Not Set')}")
            print(f"    Date: {stock.get('purchase_date', 'Unknown')}")
            if stock.get('notes'):
                print(f"    Notes: {stock['notes']}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error upgrading portfolio: {e}")
        return False

if __name__ == "__main__":
    upgrade_portfolio()
