from typing import Dict, List, Optional
from datetime import datetime
from ..markets import get_stock_price, get_monthly_prices
from ..dbmanager import DB
import time
import logging

class TradingBot:
    def __init__(self, db: DB, dbw: DB, username: str, symbols: List[str], 
                 strategy: str = 'default', interval: int = 60):
        self.db = db
        self.dbw = dbw
        self.username = username
        self.symbols = symbols
        self.strategy = strategy
        self.interval = interval  # seconds between checks
        self.running = False
        self.positions = {}
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename=f'logs/bot_{self.username}_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def start(self):
        """Start the trading bot"""
        self.running = True
        self.run()

    def stop(self):
        """Stop the trading bot"""
        self.running = False
        logging.info("Bot stopped")

    def check_balance(self) -> float:
        """Get current account balance"""
        account = self.db.get_account(self.username)
        return account['cash'] if account else 0

    def get_portfolio(self) -> Dict:
        """Get current portfolio"""
        account = self.db.get_account(self.username)
        if not account:
            return {}
        wallet = self.dbw.get_wallet(account['wallet_id'])
        return eval(wallet['portfolio']) if wallet else {}

    def analyze_market(self, symbol: str) -> Dict:
        """Analyze market conditions for a symbol"""
        price = get_stock_price(symbol)
        dates, prices = get_monthly_prices(symbol)
        
        if not price or not prices:
            return {}

        return {
            'current_price': price,
            'avg_price': sum(prices) / len(prices),
            'high': max(prices),
            'low': min(prices),
            'trend': 'up' if prices[-1] > prices[0] else 'down'
        }

    def execute_trade(self, symbol: str, action: str, quantity: float) -> bool:
        """Execute a trade"""
        if action == 'buy':
            success = self.buy_position(symbol, quantity)
        elif action == 'sell':
            success = self.sell_position(symbol, quantity)
        else:
            return False

        if success:
            logging.info(f"{action.upper()}: {quantity} {symbol}")
        return success

    def buy_position(self, symbol: str, quantity: float) -> bool:
        """Buy a position"""
        from ..wallets import buy_stock
        return buy_stock(self.db, self.dbw, self.username, symbol, quantity)

    def sell_position(self, symbol: str, quantity: float) -> bool:
        """Sell a position"""
        from ..wallets import sell_stock
        return sell_stock(self.db, self.dbw, self.username, symbol, quantity)

    def check_risk(self, symbol: str, quantity: float, price: float) -> bool:
        """Check if trade meets risk management criteria"""
        balance = self.check_balance()
        portfolio = self.get_portfolio()
        
        # Don't risk more than 2% of account on single trade
        max_risk = balance * 0.02
        trade_cost = quantity * price
        
        if trade_cost > max_risk:
            return False
            
        # Don't hold more than 20% of portfolio in single asset
        total_portfolio_value = sum(
            get_stock_price(sym) * qty 
            for sym, qty in portfolio.items()
        )
        if (trade_cost / (total_portfolio_value + balance)) > 0.2:
            return False
            
        return True

    def run(self):
        """Main bot loop"""
        while self.running:
            try:
                for symbol in self.symbols:
                    analysis = self.analyze_market(symbol)
                    if not analysis:
                        continue

                    # Simple strategy example
                    if self.strategy == 'default':
                        current = analysis['current_price']
                        avg = analysis['avg_price']
                        
                        quantity = 0.1  # Example fixed quantity
                        if current < avg * 0.95 and self.check_risk(symbol, quantity, current):
                            self.execute_trade(symbol, 'buy', quantity)
                        elif current > avg * 1.05:
                            self.execute_trade(symbol, 'sell', quantity)

                time.sleep(self.interval)
                
            except Exception as e:
                logging.error(f"Error in bot execution: {str(e)}")
                self.stop()

if __name__ == "__main__":
    # Test bot setup
    from ..dbmanager import DB
    db = DB('data/accounts.db')
    dbw = DB('data/wallets.db')
    bot = TradingBot(db, dbw, 'admin', ['AAPL', 'GOOGL'])
    bot.start()