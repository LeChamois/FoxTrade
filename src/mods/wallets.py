from mods.dbmanager import *
from mods.markets import get_stock_price
import json

def init_wallet_db(dbpath : str):
    dbw = DB(dbpath)
    dbw.create_table('wallets', {'id' : 'INTEGER PRIMARY KEY AUTOINCREMENT', 'wallet_id' : 'TEXT', 'portfolio' : 'TEXT'})
    return dbw

def dict_to_str(dict_data: dict) -> str:
    """Convert dictionary to JSON string for storage"""
    return json.dumps(dict_data)

def str_to_dict(str_data: str) -> dict:
    """Convert stored JSON string back to dictionary"""
    try:
        return json.loads(str_data) if str_data else {}
    except json.JSONDecodeError:
        return {}

def save_portfolio(dbw, wallet_id: str, portfolio: dict):
    portfolio_str = dict_to_str(portfolio)
    # Create wallet if it doesn't exist
    if not dbw.get_data_in_table('wallets', 'wallet_id', wallet_id):
        dbw.insert('wallets', {'wallet_id': wallet_id, 'portfolio': portfolio_str})
    else:
        # Need to implement update method in DB class
        pass

def add_to_portfolio(dbw, wallet_id: str, symbol: str, quantity: int):
    portfolio = get_portfolio(dbw, wallet_id)
    if symbol in portfolio:
        portfolio[symbol] += quantity
    else:
        portfolio[symbol] = quantity
    save_portfolio(dbw, wallet_id, portfolio)

def remove_from_portfolio(dbw, wallet_id: str, symbol: str, quantity: int):
    portfolio = get_portfolio(dbw, wallet_id)
    if symbol in portfolio:
        portfolio[symbol] -= quantity
        if portfolio[symbol] <= 0:
            del portfolio[symbol]
        save_portfolio(dbw, wallet_id, portfolio)

def get_portfolio(dbw, wallet_id: str) -> dict:
    result = dbw.get_data_in_table('wallets', 'wallet_id', wallet_id)
    if result and 'portfolio' in result:
        return str_to_dict(result['portfolio'])
    return {}

def create_wallet(dbw, wallet_id: str):
    if not dbw.get_data_in_table('wallets', 'wallet_id', wallet_id):
        dbw.insert('wallets', {'wallet_id' : wallet_id, 'portfolio' : '{}'})
        return True
    return False

def buy_stock(db: DB, dbw: DB, username: str, symbol: str, quantity: float) -> bool:
    """Buy stock and update portfolio"""
    account = db.get_account(username)
    if not account:
        return False

    price = get_stock_price(symbol)
    if not price:
        return False

    total_cost = price * quantity
    if account['cash'] < total_cost:
        return False

    # Get wallet and update portfolio
    wallet = dbw.get_wallet(account['wallet_id'])
    if not wallet:
        return False

    portfolio = str_to_dict(wallet['portfolio'])
    portfolio[symbol] = round(portfolio.get(symbol, 0) + quantity, 8)
    
    # Update wallet and account
    dbw.update_wallet(account['wallet_id'], dict_to_str(portfolio))
    db.update_account(username, {'cash': round(account['cash'] - total_cost, 2)})
    return True

def sell_stock(db: DB, dbw: DB, username: str, symbol: str, quantity: float) -> bool:
    """Sell stock and update portfolio"""
    account = db.get_account(username)
    if not account:
        return False

    # Get wallet and check holdings
    wallet = dbw.get_wallet(account['wallet_id'])
    if not wallet:
        return False

    portfolio = str_to_dict(wallet['portfolio'])
    if symbol not in portfolio or portfolio[symbol] < quantity:
        return False

    price = get_stock_price(symbol)
    if not price:
        return False

    total_value = price * quantity
    portfolio[symbol] = round(portfolio[symbol] - quantity, 8)
    
    # Remove symbol if quantity is 0
    if portfolio[symbol] <= 0:
        del portfolio[symbol]

    # Update wallet and account
    dbw.update_wallet(account['wallet_id'], dict_to_str(portfolio))
    db.update_account(username, {'cash': round(account['cash'] + total_value, 2)})
    return True

def get_wallet(dbw, wallet_id: str):
    return dbw.get_data_in_table('wallets', 'wallet_id', wallet_id)