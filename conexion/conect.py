import mysql.connector


conexion1=mysql.connector.connect(host="localhost", 
                                    user="root", 
                                    passwd="", 
                                    database="musicp")
cursor1=conexion1.cursor()

