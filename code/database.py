import psycopg2

class DB_conn:
    class __DB_conn:
        def __init__(self):
            t_host = "localhost" # PostgreSQL database host address,either "localhost", a domain name, or an IP address.
            t_port = "5432" # default postgres port
            t_dbname = "dbms_final_project" #database name
            t_user = "dbms_project_user" #database user name
            t_pw = "dbms_password" #password
            self.db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
        
        def __getConn(self):
            return self.db_conn

    instance = None
    def __init__(self):
        if not DB_conn.instance:
            DB_conn.instance = DB_conn.__DB_conn()

    @classmethod
    def getConn(cls):
        if not DB_conn.instance:
            cls.instance = DB_conn.__DB_conn()
        return cls.instance.__getConn()