from conect import mysql
conexion1=mysql.connector.connect(host="localhost", 
                                    user="root", 
                                    passwd="", 
                                    database="musicp")

cursor1=conexion1.cursor()



def findAll():
    cursor1.execute("select * from usuario")
    for fila in cursor1:
        print(fila)
    conexion1.close()

def findById(id):
    cursor1.execute(f"select * from usuario where id_Usuario={id}")
    for fila in cursor1:
        print(fila)
    ##conexion1.close()    

def findLogin(username,password):
    #cursor1.execute("select * from usuario where username="+username+" and password="+password)
    cursor1.execute(f"select * from usuario where username='{username}' and password='{password}'")
    for fila in cursor1:
        print(fila)
    ##conexion1.close()    

def deleteById(id):
    cursor1.execute(f"delete from usuario where id_Usuario={id}")
    conexion1.commit()
    ##conexion1.close()    

def update(id):
    #CAMBIAR SET para que sea dinamico en el update
    password='admin1'
    cursor1.execute(f"update usuario set password ='{password}' where id_Usuario={id}")
    conexion1.commit()
    ##conexion1.close() 


#PRUEBASFunciona
#findAll()
#findLogin('admin','admin')
#findById(1)
#deleteById(5)
#update(1)
