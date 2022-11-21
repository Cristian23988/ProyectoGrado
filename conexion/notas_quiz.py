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

v_table='nota_quiz'
v_id_nota_quiz='id'
v_id_sesion='id_sesion'
v_id_actividad='id_actividad'
v_id_estudiante='id_estudiante'
v_puntaje='puntaje'
v_lista_notas_quiz=[]


def findAll():
    cursor1.execute(f"select * from {v_table}")
    v_lista_notas_quiz.clear()
    for fila in cursor1:
        v_lista_notas_quiz.append(fila)

#Notas X sesion
def findById(id):
    cursor1.execute(f"select * from {v_table} where {v_id_sesion}={id}")
    
    v_lista_notas_quiz.clear()
    for fila in cursor1:
        v_lista_notas_quiz.append(fila)
    return v_lista_notas_quiz
    ##conexion1.close()    

#Notas X estudiante
def findByid_estudiante(id_estudiante):
    cursor1.execute(f"select * from {v_table} where {v_id_estudiante}={id_estudiante}")
    v_lista_notas_quiz.clear()
    for fila in cursor1:
        v_lista_notas_quiz.append(fila)
    return v_lista_notas_quiz
    ##conexion1.close()    

#Traer material o archivos de un actividad y evidencia de una nota ya calificada X ESTUDIANTE
def findByEstudiante(id_estudiante):
    ordenGet= 'est.username estudiante, e.puntaje puntaje, prof.username profesor, m.ruta '
    tables=f"{v_table} e,{v_actividad} a ,{v_material} m, {v_usuario} est, {v_usuario} prof, {v_materia} mm"
    validaciones=f"""e.id_estudiante=est.id_Usuario
                    and mm.id=a.id_materia
                    and mm.id_profesor=prof.id_Usuario
                    and e.id_actividad=a.id
                    and m.id_actividad=e.id_actividad
                    and e.id_sesion=a.id_sesion
                    and m.id_tipo_material in (1,3)
                    and e.id_estudiante={id_estudiante}"""
    sql=f"select {ordenGet} from {tables} WHERE {validaciones}"
    cursor1.execute(sql)
    v_lista_notas_quiz.clear()
    for fila in cursor1:
        v_lista_notas_quiz.append(fila)


#Traer material o archivos de un actividad y evidencia de una nota ya calificada X SESION
def findBySesion(id_sesion):
    ordenGet= 'est.username estudiante, e.puntaje puntaje, prof.username profesor, m.ruta '
    tables=f"{v_table} e,{v_actividad} a ,{v_material} m, {v_usuario} est, {v_usuario} prof, {v_materia} mm"
    validaciones=f"""e.id_estudiante=est.id_Usuario
                    and mm.id=a.id_materia
                    and mm.id_profesor=prof.id_Usuario
                    and e.id_actividad=a.id
                    and m.id_actividad=e.id_actividad
                    and e.id_sesion=a.id_sesion
                    and m.id_tipo_material in (1,3)
                    and e.id_sesion={id_sesion}"""
    sql=f"select {ordenGet} from {tables} WHERE {validaciones}"
    cursor1.execute(sql)
    v_lista_notas_quiz.clear()
    for fila in cursor1:
        v_lista_notas_quiz.append(fila)
    return v_lista_notas_quiz


def insert(id_estudiante,id_actividad,puntaje,intentos,id_sesion):
    #id_evidencia=insertar_evidencia()
    cursor1.execute(f'insert into {v_table} ({v_id_estudiante},{v_id_actividad},{v_puntaje},{v_id_sesion}) values({id_estudiante},{id_actividad},"{puntaje}",{intentos},{id_sesion})') 
    connect.conexion1.commit()

#PRUEBASFunciona
#findAll()
#findById(1)
#deleteById(5)
#update(5)}
findBySesion(7)
#insert(13, 5, 60, 1, 2)
##findByMateria(1)
#findByEstudiante(13)
print(v_lista_notas_quiz)   