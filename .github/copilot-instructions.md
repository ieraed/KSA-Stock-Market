<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Saudi Stock Market Trading Signals App - Copilot Instructions

This is a Python-based financial trading application focused on the Saudi stock market (Tadawul). When working on this project, please consider the following:

## Project Context
- This application generates buy/sell signals for Saudi stocks using technical analysis
- The main focus is on Tadawul (Saudi Stock Exchange) stocks
- Code should follow financial data analysis best practices
- Performance and real-time processing are important considerations

## Code Style Guidelines
- Use type hints for all function parameters and return values
- Follow PEP 8 style guidelines
- Use descriptive variable names, especially for financial calculations
- Add docstrings to all classes and functions
- Include error handling for data fetching and API calls

## Financial Domain Considerations
- Always validate financial data before processing
- Use appropriate decimal precision for price calculations
- Handle market hours and trading days properly
- Consider risk management in all trading logic
- Include proper logging for debugging financial calculations

## Technical Analysis Guidelines
- Use established technical indicator formulas
- Validate indicator parameters are within reasonable ranges
- Handle edge cases like insufficient data points
- Consider different timeframes (1min, 5min, 1hour, 1day)
- Implement proper signal confirmation logic

## Saudi Market Specifics
- Trading hours: Sunday to Thursday, 10:00 AM to 3:00 PM (Saudi time)
- Currency: SAR (Saudi Riyal)
- Market holidays and weekends should be considered
- Popular indices: TASI (Tadawul All Share Index)

## Dependencies and Libraries
- Use pandas for data manipulation
- Use numpy for numerical calculations
- Use ta-lib or custom implementations for technical indicators
- Use yfinance or alternative APIs for data fetching
- Use streamlit for web dashboard
- Use plotly for interactive charts

## Security Considerations
- Never hardcode API keys or sensitive data
- Use environment variables for configuration
- Validate all user inputs
- Implement proper error handling for API failures
