from .dbmanager import DB
import hashlib
import binascii
from .wallets import create_wallet

def init_account_db(dbpath: str) -> DB:
    """Initialize accounts database"""
    db = DB(dbpath)
    db.create_table('accounts', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'username': 'TEXT',
        'password': 'TEXT',
        'email': 'TEXT',
        'benefice': 'INTEGER DEFAULT 0',
        'wallet_id': 'TEXT',
        'cash': 'INTEGER DEFAULT 0'
    })
    return db

def hash_password(password: str) -> str:
    """Create SHA256 hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_account(db: DB, dbw: DB, username: str, password: str, email: str) -> bool:
    """Create new account with associated wallet"""
    if not db.get_data_in_table('accounts', 'username', username):
        wallet_id = binascii.hexlify(username.encode()).decode()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Create wallet first
        create_wallet(dbw, wallet_id)
        
        # Then create account
        db.insert('accounts', {
            'username': username,
            'password': hashed_password,
            'email': email,
            'benefice': 0,
            'wallet_id': wallet_id,
            'cash': 0
        })
        return True
    return False

def get_account(db: DB, username: str) -> dict:
    """Retrieve account data by username"""
    return db.get_data_in_table('accounts', 'username', username)

def verify_account(db: DB, username: str, password: str) -> bool:
    """Verify account credentials"""
    account = get_account(db, username)
    if account:
        hashed_password = hash_password(password)
        return account['password'] == hashed_password
    return False

def update_account(db: DB, username: str, updates: dict) -> bool:
    """Update account fields"""
    if account := get_account(db, username):
        # TODO: Implement update method in DB class
        return True
    return False