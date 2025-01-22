# src/mods/dbmanager.py
import sqlite3
from typing import Optional, Dict, List
import tabulate as tb

class DB:
    def __init__(self, dbpath : str):
        self.path = dbpath
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def update_wallet(self, wallet_id: str, portfolio: str):
        """Update wallet portfolio"""
        self.cursor.execute('UPDATE wallets SET portfolio = ? WHERE wallet_id = ?', 
                          (portfolio, wallet_id))
        self.conn.commit()

    def get_wallet(self, wallet_id: str) -> Optional[Dict]:
        """Get wallet by ID"""
        self.cursor.execute('SELECT * FROM wallets WHERE wallet_id = ?', (wallet_id,))
        result = self.cursor.fetchone()
        if result:
            return dict(zip([desc[0] for desc in self.cursor.description], result))
        return None

    def update_account(self, username: str, updates: dict):
        """Update account fields"""
        set_values = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values())
        values.append(username)
        self.cursor.execute(f'UPDATE accounts SET {set_values} WHERE username = ?', values)
        self.conn.commit()

    def get_account(self, username: str) -> Optional[Dict]:
        """Get account by username"""
        self.cursor.execute('SELECT * FROM accounts WHERE username = ?', (username,))
        result = self.cursor.fetchone()
        if result:
            return dict(zip([desc[0] for desc in self.cursor.description], result))
        return None

    def update_account(self, username: str, updates: dict):
        """Update account fields"""
        set_values = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values())
        values.append(username)
        self.cursor.execute(f'UPDATE accounts SET {set_values} WHERE username = ?', values)
        self.conn.commit()    
    def create_table(self, table_name : str, columns : Dict[str, str]):
        columns_str = ', '.join([f'{k} {v}' for k, v in columns.items()])
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})')
        self.conn.commit()

    def insert(self, table_name : str, values : Dict[str, str]):
        columns = ', '.join(values.keys())
        placeholders = ', '.join(['?' for _ in values.keys()])
        self.cursor.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})', list(values.values()))
        self.conn.commit()

    def clear_table(self, table_name : str):
        self.cursor.execute(f'DELETE FROM {table_name}')
        self.conn.commit()

    def get_table_data(self, table_name : str) -> List[Dict[str, str]]:
        self.cursor.execute(f'SELECT * FROM {table_name}')
        return [dict(zip([desc[0] for desc in self.cursor.description], row)) for row in self.cursor.fetchall()]
    
    def visualize_table(self, table_name : str):
        data = self.get_table_data(table_name)
        print(tb.tabulate(data, headers='keys', tablefmt='grid'))

    def get_data_in_table(self, table_name : str, column_name : str, value : str) -> Optional[Dict[str, str]]:
        self.cursor.execute(f'SELECT * FROM {table_name} WHERE {column_name} = ?', (value,))
        data = self.cursor.fetchone()
        if data:
            return dict(zip([desc[0] for desc in self.cursor.description], data))
        return None
    
    def close(self):
        self.conn.close()

