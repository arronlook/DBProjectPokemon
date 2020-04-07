import psycopg2

def csv_import(db_cursor,db_conn):
    # Trap errors for opening the file
    try:
        t_path_n_file = "/Users/zhangxu/Desktop/DB/final_project/DBProjectPokemon/AllMoves.csv"
        f_contents = open(t_path_n_file, 'r')
    except psycopg2.Error as e:
        t_message = "Database error: " + e + "/n open() text file: " + t_path_n_file
        return render_template("error_page.html", t_message = t_message)

    # Trap errors for copying the array to our database
    try:
        db_cursor.copy_from(f_contents, "tbl_allMoves", columns=('Name', 'Type','Category', 'Effect' , 'Power','Acc', 'PP', 'TM', 'Prob','Gen'), sep=",")
    except psycopg2.Error as e:
        t_message = "Database error: " + e + "/n copy_from"
        return render_template("error_page.html", t_message = t_message)

    # It got this far: Success!

    # Clean up by closing the database cursor and connection
    db_cursor.close()
    db_conn.close()

if __name__ == "__main__":
    t_host = "localhost" # PostgreSQL database host address,either "localhost", a domain name, or an IP address.
    t_port = "5432" # default postgres port
    t_dbname = "pokemon" #database name
    t_user = "ash" #database user name
    t_pw = "ketchum" #password
    db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
    db_cursor = db_conn.cursor()
    db_cursor.execute("DROP TABLE IF EXISTS tbl_allMoves")
    db_cursor.execute("CREATE TABLE tbl_allMoves(Name VARCHAR(256) PRIMARY KEY, Type VARCHAR(255),Category VARCHAR(255), Effect VARCHAR(255), Power VARCHAR(255),Acc VARCHAR(255),PP VARCHAR(255),TM VARCHAR(255),Prob VARCHAR(255),Gen INT)" )
    db_conn.commit()
    # db_cursor.execute("INSERT INTO tbl_allMoves(Name, Type,Category, Effect , Power,Acc, PP, TM, Prob,Gen) VALUES('10,000,000 Volt Thunderbolt','Electric','Special','Pikachu-exclusive Z-Move.',195,'-',1,null,null,7)")

    # f_contents = open('/Users/zhangxu/Desktop/DB/final_project/DBProjectPokemon/AllMoves.csv', 'r')
    # db_cursor.copy_from(f_contents, "tbl_allMoves",columns=('Name', 'Type','Category', 'Effect' , 'Power','Acc', 'PP', 'TM', 'Prob','Gen'), sep=",")
    # db_cursor.close()
    # db_conn.close()
    # csv_import(db_cursor, db_conn)




