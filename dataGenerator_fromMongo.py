import pymongo,time,os,datetime,sqlite3
#-----------------------------------------------------------------------
try:
    os.remove("DataProfit_CanalIndirecto.txt")
except:
    pass
#----------------------URI Conexion MongoDB-----------------------------
URI="mongodb://localhost:27017/"
#URI="mongodb://dbprofit1:27017/"

#------------------------Base Datos SQLite------------------------------
SQLiteconn = sqlite3.connect('profit.db')

#Eliminacion de Tabla
cursor=SQLiteconn.cursor()
cursor.execute("DROP TABLE IF EXISTS Profit_CanalIndirecto_data")
SQLiteconn.commit()
cursor.execute("DROP TABLE IF EXISTS Profit_CanalIndirecto_supervisores")
SQLiteconn.commit()

#Creacion de Table
cursor.execute("CREATE TABLE Profit_CanalIndirecto_data (idMerca text,tipoEncuesta text,fecha text,variable text,valor text,colmado text)")
SQLiteconn.commit()
cursor.execute("CREATE TABLE Profit_CanalIndirecto_supervisores (idMerca text,nombreMerca text,supervisor text,zona text)")
SQLiteconn.commit()
#-----------------------------------------------------------------
cliente = pymongo.MongoClient(URI)
db = cliente["CanalIndirecto"]
collecionDatosProfit=db["datos_profits"]
coleccionUsuariosProfit=db["usuarios_profits"]

startDate=datetime.datetime(2019,9,9)
endDate=datetime.datetime.now()

documentos=collecionDatosProfit.find({"fechaInserccion":{'$gt':startDate,'$lt':endDate}})
documentosUsuariosSupervisores=coleccionUsuariosProfit.find()
cantidad=documentos.count()
#documentos=documentos[1:200]
iteration=1
for elemento in documentos:

    #Identificacion del mercaderista
    try:
        cod_mercaderista=elemento["id"]
    except Exception as e:
        cod_mercaderista="NO DEFINIDO"
        print("Error Ocurrido")

    #Tipo de Encuesta
    try:
        tipo_encuesta=elemento["tipoEncuesta"]
    except Exception as e:
        tipo_encuesta="NO DEFINIDO"
        print("Error Ocurrido")

    #Fecha inserccion
    try:
        fecha_inserccion=elemento["fechaInserccion"]
        fecha_inserccion=fecha_inserccion.strftime("%Y-%m-%d")
    except Exception as e:
        fecha_inserccion="NO DEFINIDO"

    #Encuesta
    try:
        encuesta=str(elemento["encuesta"][0])
    except Exception as e:
        encuesta="NO DEFINIDO"

    print(str(iteration)+"---"+str(cantidad))
    iteration=iteration+1

    try:
        fileFinal=open("datosLimpios.txt","a")
        fileFinal.write(cod_mercaderista+"|"+tipo_encuesta+"|"+fecha_inserccion+"|"+encuesta+"**ENTER**")
        fileFinal.close()
    except:
        if os.path.exists("Errores.txt"):
            file1=open("Errores.txt","a")
        else:
            file1=open("Errores.txt","w")
        file1.write("Error\n")
        file1.close()
        print("Error")
        fileFinal.close()

#GENERACION DEL ARCHIVO EXCEL
#--------------------------------------------------------------------------------------------------
data=open("datosLimpios.txt").read()
dataCleanes=data.replace("%A%","").replace("\\","").replace("\"","").replace("{","").replace("}","").replace("[","").replace("]","").replace("'","")

file=open("DataToClean.txt","w")
file.write(dataCleanes)
file.close()
#--------------------------------------------------------------------------------------------------
file=open("DataToClean.txt").read().replace("encuesta:","")
vector=file.split("**ENTER**")
iteration=1
for elemento in vector:

    if len(elemento.split("|"))<2:
        continue

    print(str(iteration)+"---"+str(len(vector)))
    iteration=iteration+1

    id=elemento.split("|")[0].replace(',','')
    tipoEncuesta=elemento.split("|")[1].replace(',','')
    fechaInserccion=elemento.split("|")[2].replace(',','')
    encuesta=elemento.split("|")[3]

    #Split de los campos
    colmado="NA"
    for campo in encuesta.split(","):

        if len(campo.split(":"))<2:
            continue
        
        if campo.split(":")[0]=="colmado":
            colmado=campo.split(":")[1]

        if not os.path.exists("DataProfit_CanalIndirecto.csv"):
            filenuevo=open("DataProfit_CanalIndirecto.csv","w")
            filenuevo.close()
        filenuevo=open("DataProfit_CanalIndirecto.csv","a")
        try:
            variable=campo.split(":")[0].strip()
            valor=campo.split(":")[1].strip()
            colmado=colmado.strip()
            filenuevo.write(id+","+tipoEncuesta+","+fechaInserccion+","+campo.split(":")[0].strip()+","+campo.split(":")[1].strip()+","+colmado.strip()+"\n")
            cursor.execute("INSERT INTO Profit_CanalIndirecto_data VALUES ('"+id+"','"+tipoEncuesta+"','"+fechaInserccion+"','"+variable+"','"+valor+"','"+colmado+"')")
            print("Data Insertada en DB... "+colmado)
        except Exception as e:
            print(id)
            print(tipoEncuesta)
            print(fechaInserccion)
            print(campo)
            time.sleep(5000)
filenuevo.close()
SQLiteconn.commit()
#--------------------------------------------------------------------------------------------------
#Recolectar Supervisores
for document in documentosUsuariosSupervisores:
    print(document)
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
