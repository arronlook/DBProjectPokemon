import psycopg2
from database import DB_conn

if __name__ == "__main__":
    db_conn = DB_conn.getConn()
    db_cursor = db_conn.cursor()

    db_cursor.execute("DROP TABLE IF EXISTS tbl_allMoves")
    db_cursor.execute("CREATE TABLE tbl_allMoves(Name VARCHAR(256) PRIMARY KEY, Type VARCHAR(255),Category VARCHAR(255), Effect VARCHAR(255), Power VARCHAR(255),Acc VARCHAR(255),PP VARCHAR(255),TM VARCHAR(255),Prob VARCHAR(255),Gen INT)" )
    f_contents = open('./AllMoves_parsed.csv', 'r')
    db_cursor.copy_from(f_contents, "tbl_allMoves",columns=('Name', 'Type','Category', 'Effect' , 'Power','Acc', 'PP', 'TM', 'Prob','Gen'), sep=",")
    db_conn.commit()

    db_cursor.execute("DROP TABLE IF EXISTS tbl_pokemon")
    db_cursor.execute("CREATE TABLE tbl_pokemon(abilities VARCHAR(256), against_bug real,against_dark real,against_dragon real,against_electric real,against_fairy real,against_fight real,against_fire real,against_flying real,against_ghost real,against_grass real,against_ground real,against_ice real,against_normal real,against_poison real,against_psychic real,against_rock real,against_steel real,against_water real,attack INT,base_egg_steps INT,base_happiness INT,base_total INT,capture_rate VARCHAR(255),classfication VARCHAR(255),defense INT,experience_growth INT,height_m VARCHAR(256),hp INT,japanese_name VARCHAR(255),name VARCHAR(255) PRIMARY KEY,percentage_male VARCHAR(256),pokedex_number INT,sp_attack INT,sp_defense INT,speed INT,type1 VARCHAR(255),type2 VARCHAR(255),weight_kg VARCHAR(256),generation INT,is_legendary INT)" )
    f_contents = open('./pokemon_parsed.csv', mode='r', encoding='utf-8')
    db_cursor.copy_from(f_contents, "tbl_pokemon",columns=('abilities','against_bug','against_dark','against_dragon','against_electric','against_fairy','against_fight','against_fire','against_flying','against_ghost','against_grass','against_ground','against_ice','against_normal','against_poison','against_psychic','against_rock','against_steel','against_water','attack','base_egg_steps','base_happiness','base_total','capture_rate','classfication','defense','experience_growth','height_m','hp','japanese_name','name','percentage_male','pokedex_number','sp_attack','sp_defense','speed','type1','type2','weight_kg','generation','is_legendary'), sep=",")
    db_conn.commit()

    db_cursor.close()
    db_conn.close()





















