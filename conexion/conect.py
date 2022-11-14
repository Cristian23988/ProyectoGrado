import mysql.connector

class connect():
    conexion1=mysql.connector.connect(host="localhost", 
                                    user="root", 
                                    passwd="", 
                                    database="musicp")


