import pandas as pd
from pathlib import Path

# Create a sample portfolio Excel template
sample_data = {
    'Symbol': ['2222', '1120', '2010', '7010', '2280', '1150'],
    'Company': ['Saudi Aramco', 'Al Rajhi Bank', 'SABIC', 'STC', 'Almarai', 'Al Inma Bank'],
    'Owned_Qty': [100, 50, 75, 200, 30, 150],
    'Cost': [35.50, 85.20, 120.00, 45.30, 67.80, 28.90],
    'Custodian': ['Al Inma Capital', 'BSF Capital', 'Al Rajhi Capital', 'Al Inma Capital', 'BSF Capital', 'Al Inma Capital']
}

df = pd.DataFrame(sample_data)

# Save to Excel
current_dir = Path(__file__).parent
template_path = current_dir / "portfolio_template.xlsx"

with pd.ExcelWriter(template_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Portfolio', index=False)
    
    # Add an empty template sheet
    empty_template = pd.DataFrame({
        'Symbol': ['', '', '', '', ''],
        'Company': ['', '', '', '', ''],
        'Owned_Qty': [0, 0, 0, 0, 0],
        'Cost': [0.0, 0.0, 0.0, 0.0, 0.0],
        'Custodian': ['', '', '', '', '']
    })
    empty_template.to_excel(writer, sheet_name='Empty_Template', index=False)

print(f"✅ Portfolio template created: {template_path}")
print("📊 Sample data included with empty template sheet")
