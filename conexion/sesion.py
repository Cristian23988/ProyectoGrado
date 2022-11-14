from conect import connect 

cursor1=connect.conexion1.cursor()
v_table='sesion'
v_id_sesion='id'
v_id_materia='id_materia'
v_titulo='title'
v_corte='corte'
v_lista_sesiones=[]


def findAll():
    cursor1.execute(f"select * from {v_table}")
    v_lista_sesiones.clear()
    for fila in cursor1:
        v_lista_sesiones.append(fila)

def findById(id):
    cursor1.execute(f"select * from {v_table} where {v_id_sesion}={id}")
    
    v_lista_sesiones.clear()
    for fila in cursor1:
        v_lista_sesiones.append(fila)
    ##conexion1.close()    
#SESIONES POR MATERIA
def findByMateria(id_materia):
    cursor1.execute(f"select * from {v_table} where {v_id_materia}={id_materia}")
    v_lista_sesiones.clear()
    for fila in cursor1:
        v_lista_sesiones.append(fila)
    
    ##conexion1.close()    

def deleteById(id):
    cursor1.execute(f"delete from {v_table} where v_{v_id_sesion}={id}")
    connect.conexion1.commit()
    ##conexion1.close()    

def update(id):
    #CAMBIAR SET para que sea dinamico en el update
    titulo='Sesion3'
    cursor1.execute(f"update {v_table} set {v_titulo} ='{titulo}' where {v_id_sesion}={id}")
    connect.conexion1.commit()
    ##conexion1.close() 

def insert(titulo,id_materia,corte):
    cursor1.execute(f'insert into {v_table} ({v_titulo},{v_id_materia},{v_corte}) values("{titulo}","{id_materia},{corte}")') 
    connect.conexion1.commit()

#PRUEBASFunciona
findAll()
#findById(1)
#deleteById(5)
#update(5)
#insert('Sesion3','1')
##findByMateria(1)
print(v_lista_sesiones)   