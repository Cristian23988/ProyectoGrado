from conexion.conect import connect 
from conexion.materia import findByIdMateria

cursor1=connect.conexion1.cursor()
v_table='estudiante_materia'
v_table2='materia'
v_id_estudiante='id_estudiante'
v_id_materia='id_materia'
v_lista_materias=[]


#Materias en las que está el estudiante
def findByIdEstudiante(id):
    cursor1.execute(f"select m.* from {v_table} em, {v_table2} m  where em.id_materia=m.id AND em.{v_id_estudiante}={id}")
    v_lista_materias.clear()
    for fila in cursor1:
        v_lista_materias.append(fila) 
    return v_lista_materias


#PRUEBASFunciona
#findAll()
findByIdEstudiante(12)
#deleteById(5)
#update(1)
##insert('Clase2','Solfeo')
print(v_lista_materias)
