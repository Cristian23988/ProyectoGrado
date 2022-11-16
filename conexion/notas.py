from conexion.conect import connect 


cursor1=connect.conexion1.cursor()
#DEMAS TABLAS
v_usuario='usuario'
v_actividad='actividad'
v_sesion='sesion'
v_materia='materia'
v_evidencia='evidencia_estudiante'
v_material='material'
v_id_evidencia="id_evidencia"

#TABLA NOTAS

v_table='estudiante_nota_clase'
v_id_notas_estudiante='id'
v_id_estudiantes='id_estudiante'
v_id_actividad='id_actividad'
v_puntaje='puntaje'
v_intentos='intentos'
v_lista_estudiantes=[]


def findAll():
    cursor1.execute(f"select * from {v_table}")
    v_lista_estudiantes.clear()
    for fila in cursor1:
        v_lista_estudiantes.append(fila)

def findById(id):
    cursor1.execute(f"select * from {v_table} where {v_id_notas_estudiante}={id}")
    
    v_lista_estudiantes.clear()
    for fila in cursor1:
        v_lista_estudiantes.append(fila)
    ##conexion1.close()    

#Traer material o archivos de un actividad y evidencia de una nota ya calificada X ESTUDIANTE
def findByEstudiante(id_estudiante):
    ordenGet= '*'
    tables=f"{v_table} e, {v_evidencia} ee ,{v_actividad} a ,{v_material} m"
    validaciones=f"""m.id_actividad=a.id
                    and e.id_actividad=a.id
                    and e.id_evidencia=ee.id
                    and e.id_estudiante=ee.id_estudiante
                    and e.id_estudiante={id_estudiante}"""
    sql=f"select {ordenGet} from {tables} WHERE {validaciones}"
    cursor1.execute(f"{sql}")
    v_lista_estudiantes.clear()
    for fila in cursor1:
        v_lista_estudiantes.append(fila)

#Traer material o archivos de un actividad y evidencia de una nota ya calificada X ACTIVIDAD
def findByActividad(id_actividad):
    ordenGet= '*'
    tables=f"{v_table} e, {v_evidencia} ee ,{v_actividad} a ,{v_material} m"
    validaciones=f"""m.id_actividad=a.id
                    and e.id_actividad=a.id
                    and e.id_evidencia=ee.id
                    and e.id_estudiante=ee.id_estudiante
                    and a.id={id_actividad}"""
    sql=f"select {ordenGet} from {tables} WHERE {validaciones}"
    cursor1.execute(f"{sql}")
    v_lista_estudiantes.clear()
    for fila in cursor1:
        v_lista_estudiantes.append(fila)


#Traer material o archivos de un actividad y evidencia de una nota ya calificada X SESION
def findBySesion(id_sesion):
    ordenGet= '*'
    tables=f"{v_table} e, {v_evidencia} ee ,{v_actividad} a ,{v_material} m"
    validaciones=f"""m.id_actividad=a.id
                    and e.id_actividad=a.id
                    and e.id_evidencia=ee.id
                    and e.id_estudiante=ee.id_estudiante
                    and a.id_sesion={id_sesion}"""
    sql=f"select {ordenGet} from {tables} WHERE {validaciones}"
    cursor1.execute(f"{sql}")
    v_lista_estudiantes.clear()
    for fila in cursor1:
        v_lista_estudiantes.append(fila)

    ##conexion1.close()    
    #sql=f"select u.username,u.rol,ae.ruta, m.titulo, a.id actividad, s.corte, e.puntaje, e.intentos, p.username,p.rol , ap.descripcion_text,ap.ruta from estudiante_nota_clase e, usuario p ,actividad a ,sesion s, materia m, usuario u, material ap,material ae WHERE e.id_actividad=a.id AND m.id=s.id_materia And ae.id_sesion=a.id_sesion And ap.id_sesion=a.id_sesion AND a.id_sesion=s.id AND e.id_estudiante=u.id_Usuario AND m.id_profesor=p.id_Usuario AND ap.id_usuario=m.id_profesor AND ae.id_usuario=e.id_estudiante and ap.id_actividad=e.id_actividad and ae.id_actividad= e.id_actividad and e.id_actividad=3 and s.corte=1"



def deleteById(id):
    cursor1.execute(f"delete from {v_table} where v_{v_id_sesion}={id}")
    connect.conexion1.commit()
    ##conexion1.close()    

def update(id):
    #CAMBIAR SET para que sea dinamico en el update
    puntaje=70
    cursor1.execute(f"update {v_table} set {v_puntaje} ={puntaje} where {v_id_notas_estudiante}={id}")
    connect.conexion1.commit()
    ##conexion1.close() 


def insert(id_estudiante,id_actividad,puntaje,intentos,id_evidencia):
    #id_evidencia=insertar_evidencia()
    cursor1.execute(f'insert into {v_table} ({v_id_estudiantes},{v_id_actividad},{v_puntaje},{v_intentos},{v_id_evidencia}) values({id_estudiante},{id_actividad},"{puntaje}",{intentos},{id_evidencia})') 
    connect.conexion1.commit()

#PRUEBASFunciona
#findAll()
#findById(1)
#deleteById(5)
#update(5)
#insert(13, 5, 60, 1, 2)
##findByMateria(1)
#findByEstudiante(13)
#print(v_lista_estudiantes)   