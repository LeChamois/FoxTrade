from mods.dbmanager import *
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

def get_wallet(dbw, wallet_id: str):
    return dbw.get_data_in_table('wallets', 'wallet_id', wallet_id)