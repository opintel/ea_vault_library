
from ea_vault_library import Ea_Vault_Library
import SQLiteDB
import argparse
import gc
import sys
import os

#====================================Valores que ya deben existir====================================
sql_lite_db = SQLiteDB.SQLiteDB()
sql_lite_db.dropTable("TBL_USUARIO")
sql_lite_db.dropTable("TBL_VAULT_FILE")
sql_lite_db.createTableUsuario()
sql_lite_db.createTableVaultFile()
sql_lite_db.insertTable("TBL_USUARIO", "null,'nombre','apellido','123'")
#====================================Valores que ya deben existir====================================

parser = argparse.ArgumentParser()
parser.add_argument("--PATH", help="ruta donde se tienen los archivos guardados")
parser.add_argument("--DOC_NAME", help="nombre del archivo a guardar")
parser.add_argument("--DOC_TYPE", help="tipo de archivo : INE,CURP,ETC")
args = parser.parse_args()
PATH = args.PATH
DOC_NAME = args.DOC_NAME
DOC_TYPE = args.DOC_TYPE


def run():
    #==================================Parametros Para Clase Vault_OPI======================================INICIO
    parameters = {
        'path': PATH,
        'key': os.getenv("KEY_AES"),
         'key_private_path': os.getenv("KEY_PRIVATE_PATH"),
        'doc_name': DOC_NAME,
        'doc_type': DOC_TYPE
    }
    list_parameters=parameters["path"].split("/")
    list_parameters=list_parameters[1:-1]
    #==================================Parametros Para Clase Vault_OPI======================================FIN
    file_pdf = Ea_Vault_Library.Ea_Vault_Library(parameters)

    parameters = {
        'id_user': list_parameters[-1],
        'id_licitacion': list_parameters[-2],
        'doc_name': DOC_NAME,
        'doc_type': DOC_TYPE
    }


    if sql_lite_db.countExistValidacion(parameters) == 0:

        file_pdf.createEncryptFilePdf()

        file_pdf.createFileHash()

        file_pdf.createZipFile()

        (sql_lite_db.insertTableRawFile(
            "TBL_VAULT_FILE",
            parameters["id_licitacion"]+","+parameters["id_user"]+","+file_pdf.getAtribsFile())
        )


    for row in sql_lite_db.selectTable("TBL_VAULT_FILE", "*", "WHERE id_user={}".format(1)):

        file_pdf = Ea_Vault_Library.Ea_Vault_Library()

        file_pdf.setDocName(row[3])
        file_pdf.setKey(os.getenv("KEY_AES"))
        file_pdf.setOutputPathFile(row[5])

        file_pdf.unzipZipFile()

    gc.collect()

if __name__ == "__main__":
    run()