import psycopg2
from database import DB_conn
import csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
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
	writer = csv.writer(open('datasets/Allmoves_parsed.csv', 'w', newline=''))
	rows=[]
	with open('datasets/All_moves.csv') as f:
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
	print("Allmoves_parsed.csv created")

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

def normalize(name):
	if('-' in name):
		name= name.replace('-',' ')
	return name.lower()

def check_moves(name):
	with open('datasets/Allmoves_parsed.csv', "r", encoding='utf-8') as source:
		reader = csv.reader(source)
		for row in reader:
			name1=normalize(row[0])
			name2=normalize(name)
			if(fuzz.ratio(name1, name2)>94):
				return (1, row[0])
		return(0,name2)

def parse2():
	writer = csv.writer(open('datasets/pokemon_parsed_temp.csv', 'w', encoding="utf-8", newline=''))
	rows=[]
	with open('datasets/pokemon.csv', encoding="utf-8") as f:
		f_csv = csv.reader(f)
		headers = next(f_csv)
		for row in f_csv:
			temp=[]
			for col in row:
				(flag,col)=check2(col)
				temp.append(col)
			rows.append(temp)
	writer.writerows(rows) 
	print("pokemon_parsed_temp.csv created")


	cols_to_remove = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21,22,23] # Column indexes to be removed (starts at 0)
	cols_to_remove = sorted(cols_to_remove, reverse=True) # Reverse so we remove from the end first
	cols_to_remove2 = [0,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,38,39,40] # Column indexes to be removed (starts at 0)
	cols_to_remove2 = sorted(cols_to_remove2, reverse=True) # Reverse so we remove from the end first
	pokemon_ids=[]
	with open('datasets/pokemon_parsed_temp.csv', "r", encoding="utf-8") as source:
		reader = csv.reader(source)
		with open('datasets/pokemon_parsed_main.csv', "w", encoding="utf-8", newline='') as result:
			writer = csv.writer(result)
			for row in reader:
				if len(row) == 0:
					continue
				for col_index in cols_to_remove:
					del row[col_index]
				writer.writerow(row)
				pokemon_ids.append(row[9])
	print("pokemon_parsed_main.csv created")

	rows=[]
	with open('datasets/pokemon_parsed_temp.csv', "r", encoding="utf-8") as source2:
		reader2 = csv.reader(source2)
		with open('datasets/pokemon_parsed_weakness.csv', "w", encoding="utf-8", newline='') as result:
			writer2 = csv.writer(result)
			for row in reader2:
				if len(row) == 0:
					continue
				for col_index in cols_to_remove2:
					del row[col_index]
				if (row[-1]==''):
					row[-1]="None"
				if (row[-2]==''):
					row[-2]="None"
				if check_duplicate(row,rows)==False:
					writer2.writerow(row)
					rows.append(row)
	print("pokemon_parsed_weakness.csv created")

	pokemonid_moveid=[]
	with open('datasets/pokemon_moves.csv', "r", encoding='utf-8') as source3:
		reader3 = csv.reader(source3)
		firstline = True
		for row in reader3:
			if firstline:    #skip first line
				firstline = False
				continue
			if (row[1]=='18' and row[3]=='1' and (row[0] in pokemon_ids)):
					temp=[]
					temp.append(row[0])
					temp.append(row[2])	
					pokemonid_moveid.append(temp)

	rows=[]
	with open('datasets/moves.csv', "r", encoding='utf-8') as source4:
		reader4 = csv.reader(source4)
		firstline = True
		with open('datasets/pokemon_moves_parsed.csv', "w", encoding='utf-8', newline='') as result:
			writer3 = csv.writer(result)
			for row in reader4:
				if firstline:    #skip first line
					firstline = False
					continue
				for pid,mid in pokemonid_moveid:
					if row[0]==mid:
						(flag, name)=check_moves(row[1])
						if (flag==1):
							temp=[]
							temp.append(pid)
							temp.append(name)
							if check_duplicate(temp,rows)==False:
								writer3.writerow(temp)
								rows.append(temp)
						continue
	print("pokemon_moves_parsed.csv created")

if __name__ == "__main__":
	parse1()
	parse2()
	db_conn = DB_conn.getConn()
	db_cursor = db_conn.cursor()

	db_cursor.execute(open("schema.sql", "r").read())

	# db_cursor.execute("DROP TABLE IF EXISTS tbl_allMoves")
	# db_cursor.execute("CREATE TABLE tbl_allMoves(Name VARCHAR(256) PRIMARY KEY, Type VARCHAR(255),Category VARCHAR(255), Effect VARCHAR(255), Power VARCHAR(255),Acc VARCHAR(255),PP VARCHAR(255),TM VARCHAR(255),Prob VARCHAR(255),Gen INT)" )
	f_contents = open('datasets/Allmoves_parsed.csv', 'r')
	db_cursor.copy_from(f_contents, "tbl_allMoves",columns=('Name', 'Type','Category', 'Effect' , 'Power','Acc', 'PP', 'TM', 'prob_second_effect','Gen'), sep=",",null="")
	db_conn.commit()
	print("tbl_allMoves created")

	InsertQuery = """
                  INSERT INTO tbl_weakness (against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water, type1, type2)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  """
    with db_conn.cursor() as cursor:
        with open(findFile('datasets/pokemon_parsed_weakness.csv')[1], mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                cursor.execute(InsertQuery, tuple(row))
        db_conn.commit()
    print("tbl_weakness created")

    # db_cursor.execute("DROP TABLE IF EXISTS tbl_pokemon")
    # db_cursor.execute("CREATE TABLE tbl_pokemon(abilities VARCHAR(256), against_bug real,against_dark real,against_dragon real,against_electric real,against_fairy real,against_fight real,against_fire real,against_flying real,against_ghost real,against_grass real,against_ground real,against_ice real,against_normal real,against_poison real,against_psychic real,against_rock real,against_steel real,against_water real,attack INT,base_egg_steps INT,base_happiness INT,base_total INT,capture_rate VARCHAR(255),classfication VARCHAR(255),defense INT,experience_growth INT,height_m VARCHAR(256),hp INT,japanese_name VARCHAR(255),name VARCHAR(255) PRIMARY KEY,percentage_male VARCHAR(256),pokedex_number INT,sp_attack INT,sp_defense INT,speed INT,type1 VARCHAR(255),type2 VARCHAR(255),weight_kg VARCHAR(256),generation INT,is_legendary INT)" )
    InsertQuery = """
                  INSERT INTO tbl_pokemon (attack, classification, defense, experience_growth, height_m, hp, japanese_name, name, percentage_male, pokedex_number, sp_attack, sp_defense, speed, type1, type2, weight_kg, generation, is_legendary)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  """
    with db_conn.cursor() as cursor:
        with open(findFile('datasets/pokemon_parsed_main.csv')[1], mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                row[4] = 0 if row[4]=='' else row[4]
                row[8] = None if row[8]=='' else row[8]
                row[-3] = None if row[-3]=='' else row[-3]
                row[-1] = True if row[-1] else False
                cursor.execute(InsertQuery, tuple(row))
        db_conn.commit()
	print("tbl_pokemon created")

	f_contents = open('datasets/pokemon_moves_parsed.csv', mode='r', encoding='utf-8')
	db_cursor.copy_from(f_contents, "tbl_pokemon_moves",columns=('pokemon_id','move_name'), sep=",",null="")
	db_conn.commit()
	print("tbl_pokemon_moves created")

	db_cursor.close()
	db_conn.close()






















