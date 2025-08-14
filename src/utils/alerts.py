"""
Alert system for trading signals
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import logging
from datetime import datetime

from ..signals.signal_generator import TradingSignal

logger = logging.getLogger(__name__)

class AlertManager:
    """Manages trading signal alerts"""
    
    def __init__(self, config):
        self.config = config
        self.smtp_server = config.smtp_server
        self.smtp_port = config.smtp_port
        self.username = config.smtp_username
        self.password = config.smtp_password
        self.alert_email = config.alert_email
    
    def send_email_alert(self, signals: List[TradingSignal]) -> bool:
        """
        Send email alert for trading signals
        
        Args:
            signals: List of trading signals
        
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            if not self.alert_email or not self.username or not self.password:
                logger.warning("Email configuration incomplete. Skipping email alert.")
                return False
            
            # Create email content
            subject = f"🇸🇦 Saudi Stock Trading Signals - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            body = self._create_email_body(signals)
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = self.alert_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                text = msg.as_string()
                server.sendmail(self.username, self.alert_email, text)
            
            logger.info(f"Email alert sent successfully to {self.alert_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False
    
    def _create_email_body(self, signals: List[TradingSignal]) -> str:
        """Create HTML email body for signals"""
        
        buy_signals = [s for s in signals if s.signal_type == "BUY"]
        sell_signals = [s for s in signals if s.signal_type == "SELL"]
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: #1f4e79; color: white; padding: 10px; text-align: center; }}
                .signal-buy {{ background-color: #d4edda; color: #155724; padding: 10px; margin: 5px 0; border-left: 4px solid #28a745; }}
                .signal-sell {{ background-color: #f8d7da; color: #721c24; padding: 10px; margin: 5px 0; border-left: 4px solid #dc3545; }}
                .summary {{ background-color: #f8f9fa; padding: 10px; margin: 10px 0; }}
                .disclaimer {{ font-size: 12px; color: #6c757d; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🇸🇦 Saudi Stock Market Trading Signals</h2>
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <h3>📊 Summary</h3>
                <p>🟢 BUY signals: {len(buy_signals)}</p>
                <p>🔴 SELL signals: {len(sell_signals)}</p>
                <p>📊 Total signals: {len(signals)}</p>
            </div>
        """
        
        if buy_signals:
            html += "<h3>🟢 BUY SIGNALS</h3>"
            for signal in buy_signals:
                html += f"""
                <div class="signal-buy">
                    <strong>{signal.symbol}</strong> - {signal.price:.2f} SAR<br>
                    Confidence: {signal.confidence:.1%}<br>
                    Reason: {signal.reason}<br>
                    Time: {signal.timestamp.strftime('%Y-%m-%d %H:%M')}
                </div>
                """
        
        if sell_signals:
            html += "<h3>🔴 SELL SIGNALS</h3>"
            for signal in sell_signals:
                html += f"""
                <div class="signal-sell">
                    <strong>{signal.symbol}</strong> - {signal.price:.2f} SAR<br>
                    Confidence: {signal.confidence:.1%}<br>
                    Reason: {signal.reason}<br>
                    Time: {signal.timestamp.strftime('%Y-%m-%d %H:%M')}
                </div>
                """
        
        html += """
            <div class="disclaimer">
                <p><strong>⚠️ DISCLAIMER:</strong> These signals are for educational purposes only. 
                Always do your own research and consult with a qualified financial advisor before making investment decisions.</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def print_console_alert(self, signals: List[TradingSignal]):
        """Print alert to console"""
        print("\n" + "="*60)
        print("🔔 TRADING SIGNAL ALERT")
        print("="*60)
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Total Signals: {len(signals)}")
        
        for signal in signals:
            signal_emoji = "🟢" if signal.signal_type == "BUY" else "🔴"
            print(f"\n{signal_emoji} {signal.signal_type} {signal.symbol}")
            print(f"   💰 Price: {signal.price:.2f} SAR")
            print(f"   🎯 Confidence: {signal.confidence:.1%}")
            print(f"   💡 Reason: {signal.reason}")
        
        print("="*60)
