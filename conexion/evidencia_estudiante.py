from conexion.conect import connect 

cursor1=connect.conexion1.cursor()
v_table='evidencia_estudiante'
v_id_evidencia='id'
v_ruta='ruta'
v_id_estudiante='id_estudiante'
v_lista_usuario=[]


def findAll():
    cursor1.execute(f"select * from {v_table}")
    v_lista_usuario.clear()
    for fila in cursor1:
        v_lista_usuario.append(fila) 

def findById(id):
    cursor1.execute(f"select * from {v_table} where {v_id_evidencia}={id}")
    v_lista_usuario.clear()
    for fila in cursor1:
        v_lista_usuario.append(fila)   
def findByRuta(ruta_path):
    cursor1.execute(f'select * from {v_table} where {v_ruta}="{ruta_path}"')
    v_lista_usuario.clear()
    registro=cursor1.fetchall()
    if registro:
        return True  
    else: 
        return False    
    

def deleteById(id):
    cursor1.execute(f"delete from {v_table} where {v_id_evidencia}={id}")
    connect.conexion1.commit()
    ##conexion1.close()    

def update(id):
    #CAMBIAR SET para que sea dinamico en el update
    ruta='admin1'
    cursor1.execute(f"update {v_table} set {v_ruta} ='{ruta}' where {v_id_evidencia}={id}")
    connect.conexion1.commit()
    ##conexion1.close() 

def insert(ruta,id_estudiante):
    cursor1.execute(f'insert into {v_table} ({v_ruta},{v_id_estudiante}) values("{ruta}",{id_estudiante}) ') 
    connect.conexion1.commit()
    id = cursor1.lastrowid
    #print(id)
    return id

    
#PRUEBASFunciona
#findAll()
##findLogin('admin','admin1')
#findById(1)
#deleteById(5)
#update(1)
#insert('src/audioprueba.wav',10)
##print(v_lista_usuario)
