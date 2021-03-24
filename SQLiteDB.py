
import sqlite3
from datetime import datetime
import logging
logging.basicConfig(level=logging.DEBUG)

class SQLiteDB:
    
    def __init__(self):
        self.connection = sqlite3.connect("vault.db")
        if self.connection.total_changes == 0 :
            logging.debug("Conexión lista")
            self.cursor = self.connection.cursor()
    
    def createTableUsuario(self):
        
        query = """ 
            CREATE TABLE TBL_USUARIO (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            name_user VARCHAR(50),
            last_name_user VARCHAR(50),
            password VARCHAR(255)
            )
        """
        (self.cursor.
             execute(query)
        )
        logging.debug("Table : TBL_USUARIO creada con éxito")
        
    def createTableVaultFile(self):
        
        query = """
        CREATE TABLE TBL_VAULT_FILE (
            id_vault_file INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER, 
            id_licitacion INTEGER,
            doc_name VARCHAR(255),
            doc_type VARCHAR(50),
            output_path_file VARCHAR(255),
            hash_file VARCHAR(255),
            created_at DATETIME,
            updated_at DATETIME
            )
        """
        (self.cursor.
             execute(query)
        )

        logging.debug("Table : TBL_VAULT_FILE creada con éxito")

    def dropTable(self,tbl_name):
        self.cursor.execute("DROP TABLE {}".format(tbl_name))
        logging.debug("DROP Success")
    
    def insertTable(self,tbl_name,values):
        self.cursor.execute("INSERT INTO {} VALUES ({})".format(tbl_name,values))
        logging.debug("INSERT Success")
    
    def selectTable(self,tbl_name,columns,conditions=''):
        rows = self.cursor.execute("SELECT {} FROM {} {}".format(columns,tbl_name,conditions)).fetchall()
        """
        for item in range(len(rows)):
            print(rows[item])
        """
        return rows
    
    def foundRowsInTblVaulFile(self,parametros):
        query= """ 
         SELECT * FROM TBL_VAULT_FILE 
         WHERE id_user={} AND doc_name='{}' AND doc_type='{}' 
         """.format(parametros["id_user"],parametros["doc_name"],parametros["doc_type"])
        rows = self.cursor.execute(query).fetchall()
        print(rows)
        return rows

    def countExistValidacion(self,parametros):
        query= """ 
         SELECT COUNT(A.doc_name) FROM TBL_VAULT_FILE AS A
         INNER JOIN TBL_USUARIO AS B
         ON A.id_user = B.id_user
         WHERE A.id_user={} AND id_licitacion={} AND doc_name='{}' AND doc_type='{}' 
         GROUP BY A.doc_name
         """.format(parametros["id_user"],parametros["id_licitacion"],parametros["doc_name"],parametros["doc_type"])
        rows = self.cursor.execute(query).fetchall()
        return len(rows)

    def insertTableRawFile(self,tbl_name,values):

        self.created_at = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.updated_at = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("INSERT INTO {} VALUES (null,{})".format(tbl_name,values+",'"+ self.created_at+"','"+self.updated_at+"'"))
        logging.debug("INSERT Success")

