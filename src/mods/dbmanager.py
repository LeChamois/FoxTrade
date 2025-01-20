# src/mods/dbmanager.py
import sqlite3
from typing import Optional, Dict, List
import tabulate as tb

class DB:
    def __init__(self, dbpath : str):
        self.path = dbpath
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
    
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

