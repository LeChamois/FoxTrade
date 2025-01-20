from mods.dbmanager import *
from mods.accounts import *
from mods.wallets import *


dbw = init_wallet_db('src/data/wallets.db')
db = init_account_db('src/data/accounts.db')
db.visualize_table('accounts')
if not db.get_data_in_table('accounts', 'username', 'admin'):
    create_account(db, dbw, 'admin', 'admin*!', 'mathibard.dev@gmail.com')
else :
    print('Account already exists')
account = get_account(db, 'admin')
print(account)
wallet = get_wallet(dbw, account['wallet_id'])
print(wallet)
db.close()