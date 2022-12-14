from conexion.conect import connect 

cursor1=connect.conexion1.cursor()
v_table='material'
v_id_material='id'
v_id_tipo_material='id_tipo_material'
v_ruta='ruta'
v_descripcion_text='descripcion_text'
v_id_sesion='id_sesion'
v_id_usuario='id_usuario'
v_id_actividad='id_actividad'
v_lista_material=[]


def findAll():
    cursor1.execute(f"select * from {v_table}")
    v_lista_material.clear()
    for fila in cursor1:
        v_lista_material.append(fila) 

def findById(id):
    cursor1.execute(f"select * from {v_table} where {v_id_material}={id}")
    v_lista_material.clear()
    for fila in cursor1:
        v_lista_material.append(fila)  
    return v_lista_material

def findMaterialByActivity(id):
    #print(f"select * from {v_table} where {v_id_actividad}={id}")
    cursor1.execute(f"select * from {v_table} where {v_id_actividad}={id}")
    v_lista_material.clear()
    for fila in cursor1:
        v_lista_material.append(fila)
    return v_lista_material

def findMaterialBySesion(id):
    cursor1.execute(f"select * from {v_table} where {v_id_sesion}={id}")
    v_lista_material.clear()
    for fila in cursor1:
        v_lista_material.append(fila)
    return v_lista_material

def deleteById(id):
    cursor1.execute(f"delete from {v_table} where {v_id_material}={id}")
    connect.conexion1.commit()
    ##conexion1.close()

def deleteByIdXActividad(id):
    cursor1.execute(f"delete from {v_table} where {v_id_actividad}={id}")
    connect.conexion1.commit()
    ##conexion1.close()

def update(id_actividad, material):
    #CAMBIAR SET para que sea dinamico en el update
    #print(material)
    for fila in material:
        id=fila[0];tipo_material=fila[2];ruta=fila[1]
        cursor1.execute(f"update {v_table} set {v_ruta} ='{ruta}', id_tipo_material = {tipo_material} where {v_id_material}={id} AND id_actividad={id_actividad}")
        connect.conexion1.commit()
    ##conexion1.close() 


#Crea material asociado a la actividad
def insert(id_tipo_material,ruta,id_sesion,id_usuario,id_actividad):
    cursor1.execute(f"""insert into {v_table} ({v_id_tipo_material},{v_ruta},{v_id_sesion},{v_id_usuario},{v_id_actividad}) 
                        values({id_tipo_material},"{ruta}",{id_sesion},{id_usuario},{id_actividad}) """) 
   

    connect.conexion1.commit()
    id = cursor1.lastrowid
    #print("id del dato ingresado: ",id)
    return id

def findByRuta(ruta_path):
    cursor1.execute(f'select * from {v_table} where {v_ruta}="{ruta_path}"')
    v_lista_material.clear()
    registro=cursor1.fetchall()
    if registro:
        return True  
    else: 
        return False   

#PRUEBASFunciona
#findAll()
##findLogin('admin','admin1')
#findById(1)
#deleteById(5)
#update(1)
#insert(3,'src/audioprueba.wav','',2,2,1)
##print(v_lista_material)
