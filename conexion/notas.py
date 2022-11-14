from conect import connect 

cursor1=connect.conexion1.cursor()
v_table='estudiante_nota_clase'
v_id_notas_estudiante='id'
v_id_estudiantes='id_estudiantes'
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
##TRAER TODO ESTUDIANTE X CORTE
def findByMateria():
    cursor1.execute(f"select * from ")
    v_lista_estudiantes.clear()
    for fila in cursor1:
        v_lista_estudiantes.append(fila)
# select u.username,u.rol,ae.ruta, m.titulo, a.id actividad, s.corte, e.puntaje, e.intentos, p.username,p.rol , ap.descripcion_text,ap.ruta from estudiante_nota_clase e, usuario p ,actividad a ,sesion s, materia m, usuario u, material ap,material ae
# WHERE e.id_actividad=a.id
# AND m.id=s.id_materia
# And ae.id_sesion=a.id_sesion And ap.id_sesion=a.id_sesion
# AND a.id_sesion=s.id
# AND e.id_estudiante=u.id_Usuario
# AND m.id_profesor=p.id_Usuario
# AND ap.id_usuario=m.id_profesor AND ae.id_usuario=e.id_estudiante
# and ap.id_actividad=e.id_actividad and ae.id_actividad= e.id_actividad
# and e.id_actividad=3
# and s.corte=1
    ##conexion1.close()    

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

def insert(id_estudiantes,id_actividad,puntaje,intentos):
    cursor1.execute(f'insert into {v_table} ({v_id_estudiantes},{v_id_actividad},{v_puntaje},{v_intentos}) values({id_estudiantes},{id_actividad},{puntaje},{intentos})') 
    connect.conexion1.commit()

#PRUEBASFunciona
findAll()
#findById(1)
#deleteById(5)
#update(5)
#insert('Sesion3','1')
##findByMateria(1)
print(v_lista_estudiantes)   