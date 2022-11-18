from conexion.conect import connect 

cursor1=connect.conexion1.cursor()
cursor2=connect.conexion1.cursor()
v_table='examen_multiple'
v_table2='respuestas'
v_id_exa='id'
v_id_sesion='id_sesion'
v_id_examen='id_examen'
v_id_usuario='id_Usuario'
v_lista_examen=[]
v_lista_preguntas=[]


def findAll():
    cursor1.execute(f"select * from {v_table}")
    v_lista_examen.clear()
    for fila in cursor1:
        v_lista_examen.append(fila) 

#TRAAE EXAMENES DE LA SESIÓN

def findByIdSesion(id_sesion):
    
    cursor1.execute(f"select * from {v_table} where {v_id_sesion}={id_sesion}")
    v_lista_examen.clear()
    for fila in cursor1:
        v_lista_examen.append(fila) 
    return v_lista_examen
        
#TRAE TEXTO DE PREGUNTA Y LAS PREGUNTAS ASOCIADAS A ESE EXAMEN
#La pregunta y sus respectivas respuestas
def findById(id):
    get='id, id_sesion , texto_descripcion, ruta_imagen_descripcion'
    cursor1.execute(f"select {get} from {v_table}  where {v_id_exa}={id}")
    v_lista_examen.clear()
    for fila in cursor1:
        v_lista_examen.append(fila) 
    v_lista_preguntas.clear()
    cursor2.execute(f"select r.id,r.respuesta, r.rta from {v_table2} r where r.{v_id_examen}={id}")
    for fila2 in cursor2:
        v_lista_preguntas.append(fila2)  
    return v_lista_examen, v_lista_preguntas

def deleteById(id):
    cursor1.execute(f"delete from {v_table} where {v_id_usuario}={id}")
    connect.conexion1.commit()
    ##conexion1.close()    

#UPDATE DEBE RECIBIR ID DE EL EXAMEN
def update(id_examen_rec,descripcion_examen,ruta,lista_preguntas_recep):       
    cursor1.execute(f"update {v_table} set texto_descripcion ='{descripcion_examen}', ruta_imagen_descripcion='{ruta}' where {v_id_exa}={id_examen_rec}")
    connect.conexion1.commit()
    for fila in lista_preguntas_recep:
        id_pr=fila[0];desc=fila[1];rta=fila[3]
        cursor2.execute(f"update {v_table2} set respuesta ='{desc}', rta='{rta}' where id={id_pr} AND {v_id_examen}={id}")
        connect.conexion1.commit()
        

# def insert(usuario,passw,rol):
#     cursor1.execute(f'insert into {v_table} ({v_username},{v_password},{v_rol}) values("{usuario}","{passw}", {rol}) ') 
#     connect.conexion1.commit()


# SELECT e.id,e.id_sesion,
# e.texto_descripcion,
# e.ruta_imagen_descripcion,
# r.id,r.respuesta,
# r.rta 
# FROM examen_multiple e, respuestas r 
# WHERE e.id=r.id_examen
# and e.id_sesion=1
    
#PRUEBASFunciona
#findAll()
##findLogin('admin','admin1')
#rta=findById(1)
#deleteById(5)

#insert('prof','prof',2)
#print(rta)a
