from conexion.conect import connect 

cursor1=connect.conexion1.cursor()
v_table='usuario'
v_username='username'
v_password='password'
v_rol='rol'
v_id_usuario='id_Usuario'
v_lista_usuario=[]


def findAll():
    cursor1.execute(f"select * from {v_table}")
    v_lista_usuario.clear()
    for fila in cursor1:
        v_lista_usuario.append(fila) 

def findById(id):
    cursor1.execute(f"select * from {v_table} where {v_id_usuario}={id}")
    v_lista_usuario.clear()
    for fila in cursor1:
        v_lista_usuario.append(fila)   

def findLogin(username,password):
    #cursor1.execute("select * from usuario where username="+username+" and password="+password)
    cursor1.execute(f"select * from {v_table} where {v_username}='{username}' and {v_password}='{password}'")
    v_lista_usuario.clear()
    for fila in cursor1:
        v_lista_usuario.append(fila)  
    return v_lista_usuario 

def deleteById(id):
    cursor1.execute(f"delete from {v_table} where {v_id_usuario}={id}")
    connect.conexion1.commit()
    ##conexion1.close()    

def update(id):
    #CAMBIAR SET para que sea dinamico en el update
    password1='admin1'
    cursor1.execute(f"update {v_table} set {v_password} ='{password1}' where {v_id_usuario}={id}")
    connect.conexion1.commit()
    ##conexion1.close() 

def insert(usuario,passw,rol):
    cursor1.execute(f'insert into {v_table} ({v_username},{v_password},{v_rol}) values("{usuario}","{passw}", {rol}) ') 
    connect.conexion1.commit()

    
#PRUEBASFunciona
#findAll()
##findLogin('admin','admin1')
#findById(1)
#deleteById(5)
#update(1)
#insert('prof','prof',2)
#print(v_lista_usuario)
