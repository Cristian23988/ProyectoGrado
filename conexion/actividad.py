from conect import connect 

cursor1=connect.conexion1.cursor()
v_table='actividad'
v_id_actividad='id'
v_id_sesion='id_sesion'
v_id_profesor='id_profesor'
v_id_materia='id_materia'
v_id_tipo_actividad='id_tipo_actividad'
v_lista_actividad=[]


def findAll():
    cursor1.execute(f"select * from {v_table}")
    v_lista_actividad.clear()
    for fila in cursor1:
        v_lista_actividad.append(fila)  

def findById(id):
    cursor1.execute(f"select * from {v_table} where {v_id_actividad}={id}")
    v_lista_actividad.clear()
    for fila in cursor1:
        v_lista_actividad.append(fila)  

def deleteById(id):
    cursor1.execute(f"delete from {v_table} where v_{v_id_actividad}={id}")
    connect.conexion1.commit()
    ##conexion1.close()    

def update(id):
    #CAMBIAR SET para que sea dinamico en el update
    id_profesor=1
    cursor1.execute(f"update {v_table} set {v_id_profesor} ={id_profesor} where {v_id_actividad}={id}")
    connect.conexion1.commit()
    ##conexion1.close() 

def insert(id_sesion,id_tipo_actividad,id_materia,id_profesor):
    cursor1.execute(f'insert into {v_table} ({v_id_sesion},{v_id_tipo_actividad},{v_id_materia},{v_id_profesor}) values({id_sesion},{id_tipo_actividad},{id_materia},{id_profesor})')
    connect.conexion1.commit()

#PRUEBASFunciona
#findAll()
#findById(1)
#deleteById(5)
#update(1)
insert(3,2,1,2)
print(v_lista_actividad)
