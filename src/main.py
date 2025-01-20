from mods.dbmanager import *
from mods.accounts import *
from mods.wallets import *
from mods.markets import *
from mods.tools import *

def init_databases():
    """Initialize and return database connections"""
    try:
        dbw = init_wallet_db('src/data/wallets.db')
        db = init_account_db('src/data/accounts.db')
        return db, dbw
    except Exception as e:
        print(f"Database initialization error: {e}")
        exit(1)

def update_prices(coinlist):
    """Get updated prices for coin list"""
    updated = []
    errors = []
    for coin in coinlist:
        try:
            if price := get_stock_price(coin):
                updated.append({'symbol': coin, 'price': price})
        except Exception as e:
            errors.append(f"{coin}: {str(e)}")
    if errors:
        print("\nPrice fetch errors:")
        for error in errors:
            print(f"- {error}")
    return updated

def main():
    # Initialize databases
    db, dbw = init_databases()
    
    try:
        # Load and update coin prices
        maincoinlist = load_json_content('src/conf/maincoins.json')['basics']
        updated_coinlist = update_prices(maincoinlist)
        
        # Display current prices
        if updated_coinlist:
            print("\nCurrent Market Prices:")
            pricedict = {coin['symbol']: coin['price'] for coin in updated_coinlist}
            table_data = [{'Symbol': k, 'Price': f"${v:.2f}"} for k, v in pricedict.items()]
            show_table(table_data)
        
        # Account management
        print("\nAccount Status:")
        db.visualize_table('accounts')
        if not db.get_data_in_table('accounts', 'username', 'admin'):
            create_account(db, dbw, 'admin', 'admin*!', 'mathibard.dev@gmail.com')
        
        # Display account and wallet info
        if account := get_account(db, 'admin'):
            wallet = get_wallet(dbw, account['wallet_id'])
            if wallet:
                print("\nPortfolio Summary:")
                portfolio = str_to_dict(wallet['portfolio'])
                for symbol, amount in portfolio.items():
                    if symbol in pricedict:
                        value = amount * pricedict[symbol]
                        print(f"{symbol}: {amount} units (${value:.2f})")
    
    except Exception as e:
        print(f"Error in main execution: {e}")
    
    finally:
        db.close()
        dbw.close()

if __name__ == "__main__":
    main()