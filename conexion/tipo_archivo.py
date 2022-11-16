from conexion.conect import connect 

cursor1=connect.conexion1.cursor()
v_table='tipo_archivo'
v_id_tipo_Archivo='id'
v_id_descripcion='descripcion'
v_lista_tipos_archivo=[]


def findAll():
    cursor1.execute(f"select * from {v_table}")
    v_lista_tipos_archivo.clear()
    for fila in cursor1:
        v_lista_tipos_archivo.append(fila) 
    return v_lista_tipos_archivo

def findById(id):
    cursor1.execute(f"select * from {v_table} where {v_id_tipo_Archivo}={id}")
    v_lista_tipos_archivo.clear()
    for fila in cursor1:
        v_lista_tipos_archivo.append(fila)   
    return v_lista_tipos_archivo
    
#PRUEBASFunciona
#findAll()
##findLogin('admin','admin1')
#findById(1)
#deleteById(5)
#update(1)
#insert('prof','prof',2)
#print(v_lista_usuario)
