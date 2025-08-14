#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check portfolio cost pricing issues
"""

import pandas as pd

def check_portfolio_costs():
    """Check and fix portfolio cost pricing"""
    
    # Your real portfolio data from the attachment
    real_portfolio = [
        {"Company": "ALINMA", "Symbol": "1150", "Owned_Qty": 3722, "Cost": 27.02, "Total_Cost": 100576.73},
        {"Company": "ACIG", "Symbol": "8150", "Owned_Qty": 1500, "Cost": 15.14, "Total_Cost": 22705.72},
        {"Company": "NADEC", "Symbol": "2190", "Owned_Qty": 2967, "Cost": 22.28, "Total_Cost": 66115.55},
        {"Company": "SUMOU", "Symbol": "4323", "Owned_Qty": 1300, "Cost": 42.86, "Total_Cost": 55719.39},
        {"Company": "ALBILAD", "Symbol": "1140", "Owned_Qty": 1500, "Cost": 27.31, "Total_Cost": 40971.07},
        {"Company": "SAUDI ELECTRICITY", "Symbol": "5110", "Owned_Qty": 3000, "Cost": 17.05, "Total_Cost": 51157.95},
        {"Company": "SABIC", "Symbol": "2010", "Owned_Qty": 3000, "Cost": 71.97, "Total_Cost": 215920.33},
        {"Company": "YANSAB", "Symbol": "2290", "Owned_Qty": 3877, "Cost": 34.34, "Total_Cost": 133141.02},
        {"Company": "RETAL", "Symbol": "4322", "Owned_Qty": 4000, "Cost": 14.43, "Total_Cost": 57705.58},
        {"Company": "JARIR", "Symbol": "4190", "Owned_Qty": 8573, "Cost": 13.57, "Total_Cost": 116347.45},
        {"Company": "QACCO", "Symbol": "3040", "Owned_Qty": 972, "Cost": 62.51, "Total_Cost": 60757.55},
        {"Company": "ALBILAD SAUDI GROWTH", "Symbol": "9408", "Owned_Qty": 1000, "Cost": 11.19, "Total_Cost": 11192.68},
        {"Company": "A.OTHAIM MARKET", "Symbol": "4001", "Owned_Qty": 9500, "Cost": 10.75, "Total_Cost": 102077.59},
        {"Company": "BINDAWOOD", "Symbol": "4161", "Owned_Qty": 4000, "Cost": 7.79, "Total_Cost": 31179.70},
        {"Company": "ALAHLI REIT 1", "Symbol": "4338", "Owned_Qty": 3000, "Cost": 8.11, "Total_Cost": 24336.40},
        {"Company": "BJAZ", "Symbol": "1020", "Owned_Qty": 10546, "Cost": 13.67, "Total_Cost": 144168.86},
        {"Company": "EIC", "Symbol": "1303", "Owned_Qty": 2950, "Cost": 6.73, "Total_Cost": 15137.15},
        {"Company": "TASNEE", "Symbol": "2060", "Owned_Qty": 5500, "Cost": 10.86, "Total_Cost": 59717.67},
        {"Company": "SAVOLA GROUP", "Symbol": "2050", "Owned_Qty": 1061, "Cost": 62.74, "Total_Cost": 66564.80},
        {"Company": "SAUDI ARAMCO", "Symbol": "2222", "Owned_Qty": 2550, "Cost": 26.61, "Total_Cost": 67861.88},
        {"Company": "SAUDI DARB", "Symbol": "4130", "Owned_Qty": 2000, "Cost": 4.71, "Total_Cost": 9410.66},
        {"Company": "ALYAMAMAH STEEL", "Symbol": "1304", "Owned_Qty": 1000, "Cost": 38.69, "Total_Cost": 38693.82},
        {"Company": "SPIMACO", "Symbol": "2070", "Owned_Qty": 1500, "Cost": 31.99, "Total_Cost": 47979.34},
        {"Company": "ALMARAI", "Symbol": "2280", "Owned_Qty": 646, "Cost": 0, "Total_Cost": 1},
        {"Company": "BATIC", "Symbol": "4110", "Owned_Qty": 6800, "Cost": 2.26, "Total_Cost": 24615.27},
        {"Company": "DERAYAH", "Symbol": "4084", "Owned_Qty": 10, "Cost": 25.92, "Total_Cost": 300},
        {"Company": "MASAR", "Symbol": "4325", "Owned_Qty": 1015, "Cost": 23.34, "Total_Cost": 23346.72},
        {"Company": "SISCO HOLDING", "Symbol": "2190", "Owned_Qty": 1000, "Cost": 34.5, "Total_Cost": 28829.58},
        {"Company": "Riyadh Bank", "Symbol": "1010", "Owned_Qty": 3811, "Cost": 27.18, "Total_Cost": 105110.60},
        {"Company": "ARAMCO", "Symbol": "2222", "Owned_Qty": 231, "Cost": 24.38, "Total_Cost": 6294.75},
        {"Company": "Electrical Industries Co.", "Symbol": "1303", "Owned_Qty": 7500, "Cost": 9.03, "Total_Cost": 53454.85},
        {"Company": "Al Ahli Bank", "Symbol": "1180", "Owned_Qty": 2000, "Cost": 36.04, "Total_Cost": 66866.52},
        {"Company": "STC", "Symbol": "7010", "Owned_Qty": 3000, "Cost": 42.22, "Total_Cost": 124177.42},
        {"Company": "Arabi Bank", "Symbol": "1080", "Owned_Qty": 3666, "Cost": 21.78, "Total_Cost": 74496.43},
        {"Company": "Zain KSA", "Symbol": "7030", "Owned_Qty": 9400, "Cost": 10.9, "Total_Cost": 107214.01},
        {"Company": "SAUDI DARB", "Symbol": "4130", "Owned_Qty": 6470, "Cost": 3.12, "Total_Cost": 26000.02},
        {"Company": "ADES", "Symbol": "2382", "Owned_Qty": 1000, "Cost": 14.72, "Total_Cost": 14716.68},
        {"Company": "CHEMICAL", "Symbol": "2230", "Owned_Qty": 1000, "Cost": 7.62, "Total_Cost": 7618.62},
        {"Company": "Al Rajhi Bank", "Symbol": "1120", "Owned_Qty": 500, "Cost": 92.6, "Total_Cost": 46302.44},
    ]
    
    df = pd.DataFrame(real_portfolio)
    
    # Check for inconsistencies
    print("=== Portfolio Cost Analysis ===\n")
    
    for idx, row in df.iterrows():
        calculated_total = row['Owned_Qty'] * row['Cost']
        actual_total = row['Total_Cost']
        difference = abs(calculated_total - actual_total)
        
        if difference > 1:  # Allow for small rounding differences
            print(f"❌ {row['Company']} ({row['Symbol']}):")
            print(f"   Qty: {row['Owned_Qty']}")
            print(f"   Listed Cost: {row['Cost']}")
            print(f"   Calculated Total: {calculated_total:,.2f}")
            print(f"   Actual Total: {actual_total:,.2f}")
            print(f"   Difference: {difference:,.2f}")
            
            # Calculate what the cost should be
            correct_cost = actual_total / row['Owned_Qty']
            print(f"   ✅ Correct Cost should be: {correct_cost:.2f}\n")
        else:
            print(f"✅ {row['Company']} ({row['Symbol']}): Cost {row['Cost']} is correct")
    
    print("\n=== SISCO HOLDING Example ===")
    sisco = df[df['Symbol'] == '2190'].iloc[0]
    print(f"SISCO HOLDING:")
    print(f"  Owned Qty: {sisco['Owned_Qty']}")
    print(f"  Listed Cost: {sisco['Cost']}")
    print(f"  Total Cost: {sisco['Total_Cost']}")
    print(f"  Calculated: {sisco['Owned_Qty']} × {sisco['Cost']} = {sisco['Owned_Qty'] * sisco['Cost']}")
    print(f"  Should be: {sisco['Total_Cost']} ÷ {sisco['Owned_Qty']} = {sisco['Total_Cost'] / sisco['Owned_Qty']:.2f}")

if __name__ == "__main__":
    check_portfolio_costs()
