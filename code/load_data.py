import psycopg2
from database import DB_conn
import csv
import os

def findFile(fname):
    """
    Searches for file path recursively from ../
    @param fname is the filename to search for
    @returns (root, path to fname)
    """
    path = os.getcwd()
    breadCrumbs = fname.split("/")
    fname = breadCrumbs[-1]
    breadCrumbs[:-1]
    # To traverse potential crumbs provided
    for crumb in breadCrumbs:
        for root, dirs, files in os.walk(path):
            if crumb in dirs:
                path = os.path.join(root, crumb)
                break
    # To find the actual path    
    for root, dirs, files in os.walk(path):
        if fname in files:
            return (root, os.path.join(root, fname))
    raise FileNotFoundError("Could not find {}".format(fname))

def check1(elem):
    if len(elem)!=0:
        if ',' in elem:
            elem = elem.replace(',','\\,')
            # print(elem)
            return (1,elem)
    if (elem=='-'):
        # print(elem)
        return (1,None)
    if (elem=='∞' or elem=='âˆž'):
        return (1,999)
    return (0,elem)

def parse1():
    root, f_loc = findFile('All_moves.csv')
    writer = csv.writer(open(os.path.join(root, "Allmoves_parsed.csv"), 'w', newline=''))
    rows=[]
    with open(f_loc) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        # print(headers)
        for row in f_csv:
            temp=[]
            for col in row:
                (flag,col)=check1(col)
                # if(flag==1):
                #     # print(col)
                temp.append(col)
            rows.append(temp)
    writer.writerows(rows) 

def check2(elem):
    if len(elem)!=0:
        if ',' in elem:
            elem = elem.replace(',','\\,')
            # print(elem)
            return (1,elem)
    if (elem=='-'):
        # print(elem)
        return (1,None)
    if (elem=='30 (Meteorite)255 (Core)'):
        # print(elem)
        return (1,30)
    return (0,elem)

def check_duplicate(r, all_rows):
    t1= r[-2]
    t2= r[-1]
    for row in all_rows:
        tt1= row[-2]
        tt2= row[-1]
        if(tt1==t1 and tt2==t2):
            return True
    return False

def parse2():
    root, f_loc = findFile('datasets/pokemon.csv')
    writer = csv.writer(open(os.path.join(root, 'pokemon_parsed_temp.csv'), 'w', encoding="utf-8", newline=''))
    rows=[]

    with open(f_loc, encoding="utf-8") as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        # print(headers)
        for row in f_csv:
            temp=[]
            # print(row)
            for col in row:
                (flag,col)=check2(col)
                # if(flag==1):
                #   # print(col)
                temp.append(col)
            rows.append(temp)

    writer.writerows(rows) 

    # writer = csv.writer(open('pokemon_parsed.csv', 'w'))
    row_count=0
    cols_to_remove = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21,22,23] # Column indexes to be removed (starts at 0)
    cols_to_remove = sorted(cols_to_remove, reverse=True) # Reverse so we remove from the end first

    cols_to_remove2 = [0,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,38,39,40] # Column indexes to be removed (starts at 0)
    cols_to_remove2 = sorted(cols_to_remove2, reverse=True) # Reverse so we remove from the end first

    with open(os.path.join(root, 'pokemon_parsed_temp.csv'), "r", encoding="utf-8") as source:
        reader = csv.reader(source)
        with open(os.path.join(root, 'pokemon_parsed_main.csv'), "w", encoding="utf-8", newline='') as result:
            writer = csv.writer(result)
            for row in reader:
                if len(row) == 0:
                    continue
                row_count += 1
                # print('\r{0}'.format(row_count), end='') # Print rows processed
                for col_index in cols_to_remove:
                    del row[col_index]
                writer.writerow(row)
                # print(len(row))
    rows=[]
    with open(os.path.join(root, 'pokemon_parsed_temp.csv'), "r", encoding="utf-8") as source2:
        reader2 = csv.reader(source2)
        with open(os.path.join(root, 'pokemon_parsed_weakness.csv'), "w", encoding="utf-8", newline='') as result:
            writer2 = csv.writer(result)
            for row in reader2:
                if len(row) == 0:
                    continue
                row_count += 1
                # print('\r{0}'.format(row_count), end='') # Print rows processed
                for col_index in cols_to_remove2:
                    del row[col_index]
                if check_duplicate(row,rows)==False:
                    writer2.writerow(row)
                    rows.append(row)
        # print(len(rows))
if __name__ == "__main__":
    parse1()
    parse2()
    db_conn = DB_conn.getConn()
    db_cursor = db_conn.cursor()

    db_cursor.execute(open(findFile("schema.sql")[1], "r").read())

    # db_cursor.execute("DROP TABLE IF EXISTS tbl_allMoves")
    # db_cursor.execute("CREATE TABLE tbl_allMoves(Name VARCHAR(256) PRIMARY KEY, Type VARCHAR(255),Category VARCHAR(255), Effect VARCHAR(255), Power VARCHAR(255),Acc VARCHAR(255),PP VARCHAR(255),TM VARCHAR(255),Prob VARCHAR(255),Gen INT)" )
    f_contents = open(findFile('datasets/Allmoves_parsed.csv')[1], 'r')
    db_cursor.copy_from(f_contents, "tbl_allMoves",columns=('Name', 'Type','Category', 'Effect' , 'Power','Acc', 'PP', 'TM', 'prob_second_effect','Gen'), sep=",",null="")
    db_conn.commit()

    InsertQuery = """
                  INSERT INTO tbl_weakness (against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water, type1, type2)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  """
    with db_conn.cursor() as cursor:
        with open(findFile('datasets/pokemon_parsed_weakness.csv')[1], mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                """thing = []
                for i in range(len(row) - 2):
                    thing.append(psycopg2.extensions.Float(float(row[i])))
                thing.append(row[-2])
                thing.append(row[-1])"""
                cursor.execute(InsertQuery, tuple(row))
        db_conn.commit()

    # db_cursor.execute("DROP TABLE IF EXISTS tbl_pokemon")
    # db_cursor.execute("CREATE TABLE tbl_pokemon(abilities VARCHAR(256), against_bug real,against_dark real,against_dragon real,against_electric real,against_fairy real,against_fight real,against_fire real,against_flying real,against_ghost real,against_grass real,against_ground real,against_ice real,against_normal real,against_poison real,against_psychic real,against_rock real,against_steel real,against_water real,attack INT,base_egg_steps INT,base_happiness INT,base_total INT,capture_rate VARCHAR(255),classfication VARCHAR(255),defense INT,experience_growth INT,height_m VARCHAR(256),hp INT,japanese_name VARCHAR(255),name VARCHAR(255) PRIMARY KEY,percentage_male VARCHAR(256),pokedex_number INT,sp_attack INT,sp_defense INT,speed INT,type1 VARCHAR(255),type2 VARCHAR(255),weight_kg VARCHAR(256),generation INT,is_legendary INT)" )
    f_contents = open(findFile('datasets/pokemon_parsed_main.csv')[1], mode='r', encoding='utf-8')
    db_cursor.copy_from(f_contents, "tbl_pokemon",columns=('attack','classification','defense','experience_growth','height_m','hp','japanese_name','name','percentage_male','pokedex_number','sp_attack','sp_defense','speed','type1','type2','weight_kg','generation','is_legendary'), sep=",",null="")
    db_conn.commit()

    db_cursor.close()
    db_conn.close()






















