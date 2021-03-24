[![N|Solid](https://pythondaymx.github.io/images/opi-analytics.png)](https://nodesource.com/products/nsolid)

# How to do it

### Step 1.- Create necessary files
Crear los archivos  : 
- clave_privada.pem .- Llave privada para crear el hash verificador del archivo 
- .env
  - KEY_AES = "value"
  - RUTA = "value"
  - KEY_PRIVATE_PATH = "value"
### Step 2.- Check if the database exists
Verifcar si la base de datos esta creada , si no esta creada tener el codigo de main_example_vault.py de la siguiente forma : 
```python
    sql_lite_db = SQLiteDB.SQLiteDB()
    #sql_lite_db.dropTable("TBL_USUARIO")
    #sql_lite_db.dropTable("TBL_VAULT_FILE")
    sql_lite_db.createTableUsuario()
    sql_lite_db.createTableVaultFile()
    sql_lite_db.insertTable("TBL_USUARIO", "values")
```
De otra forma tener (esto , para evitar errores): 
```python
    sql_lite_db = SQLiteDB.SQLiteDB()
    sql_lite_db.dropTable("TBL_USUARIO")
    sql_lite_db.dropTable("TBL_VAULT_FILE")
    sql_lite_db.createTableUsuario()
    sql_lite_db.createTableVaultFile()
    sql_lite_db.insertTable("TBL_USUARIO", "values")
```
### Step 3.- Create the path where the files are saved
Crear la ruta donde se guardan los archivos (estos archivos deben generarse por manual o por sistema) , ejemplo : 
```sh
/home/opi/Documentos/Vault_OPI/vault/<value1>/<value2>/
```
### Step 4.- Install library ea_vault_library
Para instalar la librería ea_vault_library , clonar el repo e instalar con el siguiente comando el archivo con extensión .whl
```sh
 pip install <ruta>.whl
```
Nota.- Se esta suponiendo que ya se tiene levantando un venv, si aun no se cuenta con el , correr el comando : 
```sh
 python3.7 -m venv <name>
 cd bin
 source activate
```
### Step 5.- Run
Correr el proceso con : 
```sh
python main_example_vault.py --PATH="value" --DOC_NAME="value" --DOC_TYPE="value"
```
### About SQLiteDB .py
Clase desarrollada artificialmente , para simular la interacción con una base de datos , pero puede cambiarse por otra lógica y cambiarlo de igual manera en main_example_vault.py

### Nota General
Se dejan los archivos para que se pueda compilar la librería , por si se requieren hacer modificaciones.
