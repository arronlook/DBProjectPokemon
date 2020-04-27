from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
#from namespaces import all_pokemon
import psycopg2

def wilson_feature1():
    option = prompt("Select a move to see super-effectiveness>")


__functions__ = {
    "super_effective": wilson_feature1,
}

debug = False

def main():
    connection_string = "host='localhost' dbname='pokemon' user='ash' password='ketchum'"
    conn = psycopg2.connect(connection_string)
    return conn

def freezedry(conn):
    # corner case: Freeze-Dry
    # this move is super effective against Water types,
    # which usually resists Ice type moves like this one
    query = \
        "SELECT name AS Name, effect AS Effectiveness \
        FROM (\
	        SELECT name, against_ice AS effect \
            FROM tbl_pokemon\
	        WHERE against_ice > 1\
	    UNION\
	        SELECT name, (against_ice * 2) AS effect\
	        FROM tbl_pokemon\
	        WHERE (type1 = 'water' OR type2 = 'water')\
		    AND (against_ice * 2) > 1\
        ) AS freezedry ORDER BY effect DESC, name ASC"
    with conn.cursor() as cursor:
        cursor.execute(query)
        pokemon = cursor.fetchall()

    debugSum = 0
    for p in pokemon:
        if debug:
            debugSum += 1
        else:
            print(str(p[1]) + "x effective to " + p[0]) 
    if debug:
        print("Super effective to " + str(debugSum) + " Pokemon")

def flyingpress(conn):
    # corner case: Flying Press
    # this move is unique where it is two types at once
    # both types apply when calculating effectiveness
    query = \
        "SELECT name AS Name, (against_fight * against_flying) AS Effectiveness\
        FROM tbl_pokemon\
        WHERE (against_fight * against_flying) > 1\
        ORDER BY Effectiveness DESC, name ASC"
    with conn.cursor() as cursor:
        cursor.execute(query)
        pokemon = cursor.fetchall()
    debugSum = 0
    for p in pokemon:
        if debug:
            debugSum += 1
        else:
            print(str(p[1]) + "x effective to " + p[0]) 
    if debug:
        print("Super effective to " + str(debugSum) + " Pokemon")

def getType(conn, moveName):
    # minor cleaning
    if moveName.find(";") > -1:
        move = moveName[0 : moveName.find(";")].lower()
    else:
        move = moveName.lower()
    
    query = "SELECT type, category \
            FROM tbl_allMoves \
            WHERE lower(name) LIKE '%s'" % (move)
    with conn.cursor() as cursor:
        cursor.execute(query)
        moveType = cursor.fetchall()
    
    if len(moveType) != 1:
        print("No valid move specified or type received")
        return None
    else:
        if moveType[0][1] == "Status":
            print("This is a status move, no super effective type")
            return None
        else:
            #print(moveType[0][0])
            return moveType[0][0]

def testType(conn, pokemonType):
    pokeType = pokemonType.lower()
    # fighting resistance is denoted with against_fight, 
    # not against_fighting: minor check
    if pokeType.find("fighting") > -1:
        pokeType = "fight"
    
    query = "SELECT name, against_%s as effect \
        FROM tbl_pokemon\
        WHERE against_%s > 1\
        ORDER BY effect DESC, name ASC" % (pokeType, pokeType)
    with conn.cursor() as cursor:
        cursor.execute(query)
        pokemon = cursor.fetchall()
    
    if len(pokemon) == 0:
        print("No Pokemon are weak to this type")
    else:
        debugSum = 0
        for p in pokemon:
            if debug:
                debugSum += 1
            else:
                print(str(p[1]) + "x effective to " + p[0]) 
        if debug:
            print("Super effective to " + str(debugSum) + " Pokemon")

def move_query(conn, moveName):
    moveType = getType(conn, moveName)
    # if the move is a status move, nothing to be done
    # if the move doesn't exist, nothing to be done
    if moveType == None:
        #print("Invalid move specified")
        return None
    # check corner case: Freeze-Dry
    if moveName.lower() == "freeze-dry":
        freezedry(conn)
    # check corner case: Flying Press
    elif moveName.lower() == "flying press":
        flyingpress(conn)
    # any other move is valid
    else:
        testType(conn, moveType)

if __name__ == "__main__":
    # change this for quicker debugging purposes
    debug = False

    conn = main()
    #freezedry(conn)
    #flyingpress(conn)
    #testType(conn, "Poison")
    #getType(conn, "")
    #move_query(conn, "tackle")
    moveList = ["Tackle", "Flying Press", "toxic", "Nuzzle", \
                "freEzE-dRY", "; DROP TABLE tbl_pokemon; COMMIT;", \
                "instant kill", "thousand ARROWS"]
    print("Starting Tests")
    for i in range(len(moveList)):
        print("========================================")
        print("Query " + str(i + 1) + ": " + moveList[i])
        move_query(conn, moveList[i])
        print("")
    conn.close()