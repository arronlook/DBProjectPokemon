from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from database import DB_conn
from namespaces import all_moves

# change this if you don't want to see
# all of the printing
debug = False

def wilson_feature1():
    conn = DB_conn.getConn()
    moves_completer = WordCompleter(all_moves, ignore_case=True)
    print("Given a move, this will return all Pokemon that are weak to this move. It will not take into account abilities that may negate damage.")
    option = prompt("Select a move>", completer=moves_completer)
    move_query_weak(conn, option)

def wilson_feature2():
    conn = DB_conn.getConn()
    moves_completer = WordCompleter(all_moves, ignore_case=True)
    print("Given a move, this will return all Pokemon that resist this move. It will not take into account abilities that may reduce damage.")
    option = prompt("Select a move>", completer=moves_completer)
    move_query_strong(conn, option)

__functions__ = {
    "super_effective": wilson_feature1,
    "not_effective": wilson_feature2,
}

def main():
    connection_string = "host='localhost' dbname='pokemon' user='ash' password='ketchum'"
    conn = psycopg2.connect(connection_string)
    return conn

def freezedry(conn, isWeak):
    # corner case: Freeze-Dry
    # this move is super effective against Water types,
    # which usually resists Ice type moves like this one
    # 0.5x to 2x is a 4x increase
    if isWeak:
        # find pokemon super effective to this move
        query = \
            "SELECT type1, type2, against_ice \
            FROM (\
                SELECT type1, type2, against_ice \
                FROM tbl_weakness \
                WHERE against_ice > 1 \
            UNION \
                SELECT type1, type2, (against_ice * 4) AS against_ice \
                FROM tbl_weakness \
                WHERE (type1 = 'water' OR type2 = 'water') \
                AND (against_ice * 4) > 1\
            ) AS freezedry ORDER BY against_ice DESC, type1, type2"
    else:
        # find pokemon that resist this move
        query = \
            "SELECT type1, type2, against_ice \
            FROM (\
                SELECT type1, type2, against_ice \
                FROM tbl_weakness \
                WHERE against_ice < 1 \
                AND type1 != 'water' AND type2 != 'water'\
            UNION \
                SELECT type1, type2, (against_ice * 4) AS against_ice \
                FROM tbl_weakness \
                WHERE (type1 = 'water' OR type2 = 'water') \
                AND (against_ice * 4) < 1\
            ) AS freezedry ORDER BY against_ice ASC, type1, type2"
    with conn.cursor() as cursor:
        cursor.execute(query)
        types = cursor.fetchall()
    if len(types) == 0:
        # no pokemon are weak to or resist this move
        return None
    return types

def flyingpress(conn, isWeak):
    # corner case: Flying Press
    # this move is unique where it is two types at once
    # both types apply when calculating effectiveness
    if isWeak:
        query = \
            "SELECT type1, type2, (against_fight * against_flying) as effect\
            FROM tbl_weakness \
            WHERE (against_fight * against_flying) > 1 \
            ORDER BY effect DESC, type1, type2"
    else:
        query = \
            "SELECT type1, type2, (against_fight * against_flying) as effect\
            FROM tbl_weakness \
            WHERE (against_fight * against_flying) < 1 \
            ORDER BY effect ASC, type1, type2"
    with conn.cursor() as cursor:
        cursor.execute(query)
        types = cursor.fetchall()
    if len(types) == 0:
        # no pokemon are weak to this move
        return None
    return types

def getType(conn, moveName):
    # minor cleaning of SQL injection
    if moveName.find(";") > -1:
        move = moveName[0 : moveName.find(";")].lower()
    else:
        move = moveName.lower()
    
    # not case-sensitive search
    query = "SELECT type, category \
            FROM tbl_allMoves \
            WHERE lower(name) LIKE '%s'" % (move)
    with conn.cursor() as cursor:
        cursor.execute(query)
        moveType = cursor.fetchall()
    
    # if 0, no matching moves
    # if >1, too many moves returned
    # should only return 1 move
    if len(moveType) != 1:
        print("No valid move specified received")
        return None
    else:
        if moveType[0][1] == "Status":
            print("This is a status move, no super effective type")
            return None
        else:
            #print(moveType[0][0])
            return moveType[0][0]

def checkType(conn, pokemonType, isWeak):
    pokeType = pokemonType.lower()
    # fighting resistance is denoted with against_fight, 
    # not against_fighting: minor check
    if pokeType.find("fighting") > -1:
        pokeType = "fight"

    if isWeak:
        query = \
            "SELECT type1, type2, against_%s \
            FROM tbl_weakness \
            WHERE against_%s > 1\
            ORDER BY against_%s DESC, type1, type2" % (pokeType, pokeType, pokeType)
    else:
        query = \
            "SELECT type1, type2, against_%s \
            FROM tbl_weakness \
            WHERE against_%s < 1\
            ORDER BY against_%s DESC, type1, type2" % (pokeType, pokeType, pokeType)
    with conn.cursor() as cursor:
        cursor.execute(query)
        types = cursor.fetchall()
    if len(types) == 0:
        return None
    return types

def printPokemonWeak(conn, types):
    if types is None:
        print("No Pokemon are weak to this move")
        return None
    # lists of super effectiveness
    effectx4 = []
    effectx2 = []
    for t in types:
        query = "SELECT name, type1, type2 \
            FROM tbl_pokemon \
            WHERE lower(type1) = '%s' \
            AND lower(type2) = '%s'" % (str(t[0]), str(t[1]))
        with conn.cursor() as cursor:
            cursor.execute(query)
            pokemon = cursor.fetchall()
        if len(pokemon) != 0:
            for p in pokemon:
                if t[2] == 4.0:
                    effectx4.append(str(p[0]))
                elif t[2] == 2.0:
                    effectx2.append(str(p[0]))
    # sort the lists alphabetically
    effectx4.sort()
    effectx2.sort()
    if len(effectx4) + len(effectx2) == 0:
        print("No Pokemon are weak to this move")
    else:
        # print in order of effectiveness, then alphabetically
        # this makes it easier to find a pokemon by name
        for i in range(len(effectx4)):
            print("4.0x effective to " + effectx4[i])
        for i in range(len(effectx2)):
            print("2.0x effective to " + effectx2[i])

def printPokemonStrong(conn, types):
    if types is None:
        print("No Pokemon resist this move")
        return None
    # lists of not very effectiveness
    effectx_0 = []
    effectx_4 = []
    effectx_2 = []
    for t in types:
        query = "SELECT name, type1, type2 \
            FROM tbl_pokemon \
            WHERE lower(type1) = '%s' \
            AND lower(type2) = '%s'" % (str(t[0]), str(t[1]))
        with conn.cursor() as cursor:
            cursor.execute(query)
            pokemon = cursor.fetchall()
        if len(pokemon) != 0:
            for p in pokemon:
                if t[2] == 0.0:
                    effectx_0.append(str(p[0]))
                elif t[2] == 0.25:
                    effectx_4.append(str(p[0]))
                elif t[2] == 0.5:
                    effectx_2.append(str(p[0]))
    # sort the lists alphabetically
    effectx_0.sort()
    effectx_4.sort()
    effectx_2.sort()
    if len(effectx_0) + len(effectx_4) + len(effectx_2) == 0:
        print("No Pokemon resist this move")
    else:
        # print in order of effectiveness, then alphabetically
        # this makes it easier to find a pokemon by name
        for i in range(len(effectx_0)):
            print("No effect to " + effectx_0[i])
        for i in range(len(effectx_4)):
            print("0.25x effective to " + effectx_4[i])
        for i in range(len(effectx_2)):
            print("0.5x effective to " + effectx_2[i])

def move_query_weak(conn, moveName):
    moveType = getType(conn, moveName)
    # if the move is a status move, nothing to be done
    # if the move doesn't exist, nothing to be done
    if moveType == None:
        #print("Invalid move specified")
        return None
    # check corner case: Freeze-Dry
    if moveName.lower() == "freeze-dry":
        types = freezedry(conn, True)
    # check corner case: Flying Press
    elif moveName.lower() == "flying press":
        types = flyingpress(conn, True)
    # any other move is valid
    else:
        types = checkTypeWeak(conn, moveType, True)
    
    printPokemonWeak(conn, types)

def move_query_strong(conn, moveName):
    moveType = getType(conn, moveName)
    # if the move is a status move, nothing to be done
    # if the move doesn't exist, nothing to be done
    if moveType == None:
        #print("Invalid move specified")
        return None
    # check corner case: Freeze-Dry
    if moveName.lower() == "freeze-dry":
        types = freezedry(conn, False)
    # check corner case: Flying Press
    elif moveName.lower() == "flying press":
        types = flyingpress(conn, False)
    # any other move is valid
    else:
        types = checkType(conn, moveType, False)
    printPokemonStrong(conn, types)

if __name__ == "__main__":
    conn = main()
    # testing
    moveList = ["Tackle", "Flying Press", "toxic", "Nuzzle", \
                "freEzE-dRY", "; DROP TABLE tbl_pokemon; COMMIT;", \
                "instant kill", "thousand ARROWS", "shIFt gEaR", \
                "geAR gRInD"]
    print("Starting Tests")
    for i in range(len(moveList)):
        print("========================================")
        print("Query " + str(i + 1) + ": " + moveList[i])
        move_query(conn, moveList[i])
        print("")
    
    conn.close()