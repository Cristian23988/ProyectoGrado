from conect import connect 

cursor1=connect.conexion1.cursor()
v_table='materia'
v_id_materia='id'
v_titulo='titulo'
v_descripcion='descripcion'
v_id_profesor='id_profesor'
v_lista_materias=[]


def findAll():
    cursor1.execute(f"select * from {v_table}")
    v_lista_materias.clear()
    for fila in cursor1:
        v_lista_materias.append(fila)  

def findById(id):
    cursor1.execute(f"select * from {v_table} where {v_id_materia}={id}")
    v_lista_materias.clear()
    for fila in cursor1:
        v_lista_materias.append(fila)  

def deleteById(id):
    cursor1.execute(f"delete from {v_table} where v_{v_id_materia}={id}")
    connect.conexion1.commit()
    ##conexion1.close()    

def update(id):
    #CAMBIAR SET para que sea dinamico en el update
    titulo='Clase2'
    cursor1.execute(f"update {v_table} set {v_titulo} ='{titulo}' where {v_id_materia}={id}")
    connect.conexion1.commit()
    ##conexion1.close() 

def insert(titulo,descripcion,id_profesor):
    cursor1.execute(f'insert into {v_table} ({v_titulo},{v_descripcion},{v_id_profesor}) values("{titulo}","{descripcion},{id_profesor}")') 
    connect.conexion1.commit()

#PRUEBASFunciona
findAll()
#findById(1)
#deleteById(5)
#update(1)
##insert('Clase2','Solfeo')
print(v_lista_materias)
