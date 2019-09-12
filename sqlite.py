import pymongo,time,os,datetime,sqlite3
#-----------------------------------------------------------------------
try:
    os.remove("DataProfit_CanalIndirecto.txt")
except:
    pass
#------------------------Base Datos SQLite------------------------------
SQLiteconn = sqlite3.connect('profit.db')

#Eliminacion de Tabla
cursor=SQLiteconn.cursor()
cursor.execute("DROP TABLE IF EXISTS Profit_CanalIndirecto_supervisores")
SQLiteconn.commit()

#Creacion de Table
cursor.execute("CREATE TABLE Profit_CanalIndirecto_supervisores (idMerca text,nombreMerca text,supervisor text,zona text)")
SQLiteconn.commit()

#----------------------URI Conexion MongoDB-----------------------------
URI="mongodb://localhost:27017/"
#URI="mongodb://dbprofit1:27017/"

cliente = pymongo.MongoClient(URI)
db = cliente["CanalIndirecto"]
collecionDatosProfit=db["datos_profits"]
coleccionUsuariosProfit=db["usuarios_profits"]

startDate=datetime.datetime(2019,9,9)
endDate=datetime.datetime.now()

documentos=collecionDatosProfit.find({"fechaInserccion":{'$gt':startDate,'$lt':endDate}})
documentosUsuariosSupervisores=coleccionUsuariosProfit.find()
cantidad=documentos.count()

#--------------------------------------------------------------------------------------------------
#Recolectar Supervisores
for document in documentosUsuariosSupervisores:
    print("Insertado...")
    identificador=str(document['identificador'])
    nombreMerca=document['nombre']
    supervisor=document['supervisor']
    zona=document['zona']
    cursor.execute("INSERT INTO Profit_CanalIndirecto_supervisores VALUES ('"+identificador+"','"+nombreMerca+"','"+supervisor+"','"+zona+"')")


SQLiteconn.commit()
SQLiteconn.close()
#--------------------------------------------------------------------------------------------------
#LIMPIEZA DE ARCHIVO
if os.path.exists(os.getcwd()+"\\DataToClean.txt"):
    os.remove("DataToClean.txt")
if os.path.exists(os.getcwd()+"\\datosLimpios.txt"):
    os.remove("datosLimpios.txt")
if os.path.exists(os.getcwd()+"\\Errores.txt"):
    os.remove("Errores.txt")
