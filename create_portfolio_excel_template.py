"""
📊 Portfolio Excel Template Creator
Creates a comprehensive Excel template for portfolio data import
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def create_portfolio_excel_template():
    """Create a comprehensive Excel template with sample data and instructions"""
    
    # Sample portfolio data with real Saudi stocks
    sample_data = {
        'symbol': ['1010', '1020', '1080', '1140', '1150', '1180', '1120', 
                  '2222', '2010', '4001', '1303', '1304', '2030', '2020', '1211'],
        'quantity': [1000, 500, 750, 1200, 800, 600, 300, 
                    400, 1500, 250, 2000, 1000, 350, 450, 180],
        'purchase_price': [25.50, 45.20, 67.80, 18.75, 32.40, 45.60, 125.80,
                          85.30, 28.90, 180.50, 15.20, 22.40, 95.60, 78.20, 155.30],
        'purchase_date': ['2024-01-15', '2024-02-20', '2024-03-10', '2024-01-25', 
                         '2024-02-05', '2024-03-15', '2024-01-30',
                         '2024-02-12', '2024-03-08', '2024-01-18', 
                         '2024-02-28', '2024-03-05', '2024-01-22', '2024-02-15', '2024-03-12'],
        'broker': ['Al Rajhi Capital', 'SNB Capital', 'Alinma Investment', 
                  'NCB Capital', 'Riyad Capital', 'Al Fransi Capital',
                  'Al Rajhi Capital', 'SABB Capital', 'Jadwa Investment',
                  'EFG Hermes', 'Albilad Investment', 'Derayah Financial',
                  'Mubasher Capital', 'Al Ahli Capital', 'Falcom Financial']
    }
    
    # Create main portfolio DataFrame
    portfolio_df = pd.DataFrame(sample_data)
    
    # Create instructions DataFrame
    instructions_data = {
        'Field': ['symbol', 'quantity', 'purchase_price', 'purchase_date', 'broker'],
        'Description': [
            'Stock symbol (e.g., 1010, 2222, 4001)',
            'Number of shares owned',
            'Purchase price per share in SAR',
            'Purchase date (YYYY-MM-DD format)',
            'Broker name (optional)'
        ],
        'Example': ['1010', '1000', '25.50', '2024-01-15', 'Al Rajhi Capital'],
        'Required': ['Yes', 'Yes', 'Yes', 'Yes', 'No']
    }
    
    instructions_df = pd.DataFrame(instructions_data)
    
    # Create stock reference DataFrame with popular stocks
    stock_reference_data = {
        'Symbol': ['1010', '1020', '1080', '1120', '1140', '1150', '1180', 
                  '2222', '2010', '2020', '2030', '4001', '1303', '1304', '1211'],
        'Company Name': [
            'Riyad Bank', 'Bank AlJazira', 'Arab National Bank', 'Al Rajhi Bank',
            'Al Bilad Bank', 'Alinma Bank', 'Saudi National Bank',
            'Saudi Aramco', 'Saudi Fertilizers', 'SABIC', 'SABIC Agri-Nutrients',
            'Jarir Marketing', 'Electrical Industries', 'Al Yamamah Steel',
            'Saudi Investment Bank'
        ],
        'Sector': [
            'Banking', 'Banking', 'Banking', 'Banking', 'Banking', 'Banking', 'Banking',
            'Energy', 'Materials', 'Materials', 'Materials',
            'Consumer Discretionary', 'Industrial', 'Materials', 'Banking'
        ]
    }
    
    stock_reference_df = pd.DataFrame(stock_reference_data)
    
    # Create broker reference DataFrame
    broker_reference_data = {
        'Broker Name': [
            'Al Rajhi Capital', 'SNB Capital', 'Alinma Investment', 'NCB Capital',
            'Riyad Capital', 'Al Fransi Capital', 'SABB Capital', 'Jadwa Investment',
            'EFG Hermes', 'Albilad Investment', 'Derayah Financial', 'Mubasher Capital',
            'Al Ahli Capital', 'Falcom Financial', 'Saudi Investment Company'
        ],
        'Type': [
            'Full Service', 'Full Service', 'Full Service', 'Full Service',
            'Full Service', 'Full Service', 'Full Service', 'Full Service',
            'Full Service', 'Full Service', 'Online', 'Online',
            'Full Service', 'Full Service', 'Full Service'
        ]
    }
    
    broker_reference_df = pd.DataFrame(broker_reference_data)
    
    # Create Excel file with multiple sheets
    filename = f"Portfolio_Template_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Write main portfolio template
        portfolio_df.to_excel(writer, sheet_name='Portfolio_Template', index=False)
        
        # Write instructions
        instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
        
        # Write stock reference
        stock_reference_df.to_excel(writer, sheet_name='Stock_Reference', index=False)
        
        # Write broker reference
        broker_reference_df.to_excel(writer, sheet_name='Broker_Reference', index=False)
        
        # Create empty template for user data
        empty_template = pd.DataFrame(columns=['symbol', 'quantity', 'purchase_price', 'purchase_date', 'broker'])
        empty_template.to_excel(writer, sheet_name='Your_Portfolio', index=False)
        
        # Get workbook and worksheets for formatting
        workbook = writer.book
        
        # Format Portfolio_Template sheet
        ws_portfolio = writer.sheets['Portfolio_Template']
        ws_portfolio.title = "📊 Sample Portfolio"
        
        # Format Instructions sheet
        ws_instructions = writer.sheets['Instructions']
        ws_instructions.title = "📋 Instructions"
        
        # Format Stock Reference sheet
        ws_stock_ref = writer.sheets['Stock_Reference']
        ws_stock_ref.title = "📈 Stock Reference"
        
        # Format Broker Reference sheet
        ws_broker_ref = writer.sheets['Broker_Reference']
        ws_broker_ref.title = "🏦 Broker Reference"
        
        # Format Your Portfolio sheet
        ws_your_portfolio = writer.sheets['Your_Portfolio']
        ws_your_portfolio.title = "💼 Your Portfolio"
        
        # Auto-adjust column widths
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print(f"✅ Excel template created: {filename}")
    print("\n📊 Template Contents:")
    print("• 📊 Sample Portfolio - Example data with 15 Saudi stocks")
    print("• 📋 Instructions - Field descriptions and requirements")
    print("• 📈 Stock Reference - Popular Saudi stock symbols and names")
    print("• 🏦 Broker Reference - Common Saudi brokers")
    print("• 💼 Your Portfolio - Empty template for your data")
    print("\n🎯 How to use:")
    print("1. Open the Excel file")
    print("2. Go to 'Your Portfolio' sheet")
    print("3. Enter your stock data")
    print("4. Save as CSV and upload to the app")
    print("\n💡 Tips:")
    print("• Use the Stock Reference sheet to find correct symbols")
    print("• Check the Sample Portfolio for data format examples")
    print("• The broker field is optional but recommended")
    
    return filename

if __name__ == "__main__":
    create_portfolio_excel_template()
