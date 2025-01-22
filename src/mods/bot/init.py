from mods.dbmanager import *

def init_bot_databases():
    dbot = DB('src/data/bot.db')
    dbot.create_table('bots', {'bot_id': 'TEXT PRIMARY KEY', 'name': 'TEXT', 'settings': 'TEXT'})
    return dbot
