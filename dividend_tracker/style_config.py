def style_dividend_table(df):
    return df.style.set_properties(**{
        'background-color': '#f9f9f9',
        'color': '#333',
        'border-color': '#ccc'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('background-color', '#004c97'), ('color', 'white')]
    }])
