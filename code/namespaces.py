"""
Useful suggestion hints we might want to use
"""
from database_conn import DB_conn

conn = DB_conn.getConn()

# all_pokemon is a list of all pokemon
query = "SELECT name FROM tbl_pokemon"
all_pokemon = []
cursor = conn.cursor()
with cursor as cursor:
    cursor.execute(query)
    res = cursor.fetchall()
    for r in res:
        all_pokemon.append(r[0])

# all_moves is a list of all moves
query = "SELECT Name FROM tbl_allmoves"
all_moves = []
cursor = conn.cursor()
with cursor as cursor:
    cursor.execute(query)
    res = cursor.fetchall()
    for r in res:
        all_moves.append(r[0])

all_types = [
    "normal",
    "water",
    "electric",
    "fighting",
    "ground",
    "psychic",
    "rock",
    "dark",
    "steel",
    "fire",
    "grass",
    "ice",
    "poison",
    "flying",
    "bug",
    "ghost",
    "dragon",
    "fairy"
]

all_stats = [
    "hp",
    "attack",
    "sp_attack",
    "defense",
    "sp_defense",
    "speed"
]