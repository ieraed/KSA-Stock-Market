"""
Configuration management for the Saudi Stock Market Trading Signals App
"""

import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration class for the trading signals app"""
    
    # Database configuration
    database_url: str = "sqlite:///trading_signals.db"
    
    # API configuration
    api_key: str = ""
    
    # Alert configuration
    alert_email: str = ""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    
    # Trading configuration
    rsi_period: int = 14
    rsi_oversold: float = 30.0
    rsi_overbought: float = 70.0
    
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    
    bb_period: int = 20
    bb_std_dev: float = 2.0
    
    sma_short: int = 10
    sma_long: int = 50
    
    # Data fetching configuration
    default_period: str = "1y"
    default_interval: str = "1d"
    
    def __init__(self):
        """Initialize configuration from environment variables"""
        self.database_url = os.getenv("DATABASE_URL", self.database_url)
        self.api_key = os.getenv("API_KEY", self.api_key)
        self.alert_email = os.getenv("ALERT_EMAIL", self.alert_email)
        self.smtp_server = os.getenv("SMTP_SERVER", self.smtp_server)
        self.smtp_port = int(os.getenv("SMTP_PORT", str(self.smtp_port)))
        self.smtp_username = os.getenv("SMTP_USERNAME", self.smtp_username)
        self.smtp_password = os.getenv("SMTP_PASSWORD", self.smtp_password)
    
    def get_trading_params(self) -> Dict[str, Any]:
        """Get trading-related parameters"""
        return {
            "rsi_period": self.rsi_period,
            "rsi_oversold": self.rsi_oversold,
            "rsi_overbought": self.rsi_overbought,
            "macd_fast": self.macd_fast,
            "macd_slow": self.macd_slow,
            "macd_signal": self.macd_signal,
            "bb_period": self.bb_period,
            "bb_std_dev": self.bb_std_dev,
            "sma_short": self.sma_short,
            "sma_long": self.sma_long,
        }
    
    def get_saudi_market_hours(self) -> Dict[str, str]:
        """Get Saudi market trading hours"""
        return {
            "start_time": "10:00",
            "end_time": "15:00",
            "timezone": "Asia/Riyadh",
            "trading_days": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        }
