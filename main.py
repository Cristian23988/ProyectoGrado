from ctypes import pointer
import sys
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QComboBox, QLabel, QPlainTextEdit, QFrame, QGridLayout, QPushButton, QScrollArea, QApplication, QSpacerItem,
                             QHBoxLayout, QVBoxLayout, QMainWindow, QSizePolicy, QMessageBox)
from PyQt5.QtCore import *
from PyQt5 import uic # llama al archivo disenofinal.ui
from PyQt5 import QtWidgets
import functools
import numpy as np
import librosa
import midiutil
from music21 import note, stream
from sound_to_midi.monophonic import wave_to_midi
from pdf2image import convert_from_path
import aspose.words as aw
import partitureConversion.main 
import sys
import subprocess
import cv2
import time
import numpy as np
from partitureConversion.best_fit import fit
from partitureConversion.rectangle import Rectangle
from partitureConversion.note import Note
from random import randint
import threading
import time
from partitureConversion.MIDIUtil.src.midiutil.MidiFile3 import MIDIFile
from Comparacion.compare import comparacion_wav
from conexion.evidencia_estudiante import insert as insertar_evidencia
from conexion.evidencia_estudiante import findByRuta as existeEvidencia
from conexion.material_actividad import findByRuta as existematerial
from conexion.notas import insert as insertarNota
from conexion.material_actividad import insert as insertar_materialXactividad
from conexion.user import findLogin
from conexion.materia import findAll as materiaFindAll
from conexion.sesion import findByMateria as sesionFindAll
from conexion.sesion import findById as sesionFindId
from conexion.sesion import insert as insertSesiones
from conexion.sesion import update as updateSesiones
from conexion.actividad import findBySesion as actividadFindAll
from conexion.material_actividad import findMaterialByActivity as materialByActividad
from conexion.material_actividad import findById as materialById
from conexion.material_actividad import deleteById as deleteMaterial
from conexion.preguntas import update as actualizar_preguntas
from conexion.tipo_archivo import findById as tipoArchivo
from conexion.material_actividad import insert as guardarMateria_Actividad
from conexion.actividad import update as actualizar_actividad
from conexion.actividad import insert as insertar_actividad
from conexion.actividad import findById as actividadFindId
from conexion.actividad import findTipoActividades as findTipoActividad
from conexion.tipo_archivo import findById as tipoArchivo
from conexion.preguntas import update as actualizar_preguntas


s = stream.Stream()
        
class Ventana(QMainWindow):
    
    def __init__(self):
        super(Ventana, self).__init__()
        uic.loadUi("ui/login.ui", self)  #P1: mostraba la GUI  disenofinal.ui
        self.button_login.clicked.connect(lambda:self.logIn(self.input_login_correo.text(),self.input_login_contrasena.text()))
        v_id_usuario = 0
        v_usuarioN = ""
        v_rolN = ""
        v_table = None
        v_id_materia = 0
        v_id_sesion = 0
        v_id_actividad = 0

    def logIn(self,userName,password):
        if userName and password:
            user = findLogin(userName,password)
            if user and user[0][3] == 2:
                print('Estas logeado')
                self.v_id_usuario=user[0][0]
                self.v_usuarioN = user[0][1]
                self.v_rolN = "Profesor"
                self.profesor()
            elif user and user[0][3] == 3:
                print('Estas logeado')
                self.v_id_usuario=user[0][0]
                self.v_usuarioN = user[0][1]
                self.v_rolN = "Estudiante"
                self.estudiante()
            else:
                print('No estas logeado')
    
    def cerrarSesion(self):
        uic.loadUi("ui/login.ui", self)  #P1: mostraba la GUI  disenofinal.ui
        self.input_login_correo.setText("")
        self.input_login_contrasena.setText("")
        self.button_login.clicked.connect(lambda:self.logIn(self.input_login_correo.text(),self.input_login_contrasena.text()))

    def estudiante(self):
        uic.loadUi("ui/diseno_estudiante.ui", self)  #P1: mostraba la GUI  disenofinal.ui
        self.stackedWidget.setCurrentWidget(self.page_home)
        self.label_userName.setText(self.v_usuarioN)
        self.label_userRole.setText(self.v_rolN)
        self.button_menu_cerrar_sesion.clicked.connect(self.cerrarSesion)
        self.button_practicas_record.clicked.connect(self.grabar_estudiante)
        self.button_compare.clicked.connect(self.prueba_compare)
        ##self.button_menu_teoria.clicked.connect(self.Abrir_Modulo_Teoria)

        self.button_menu_practicas.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_practicas))
        self.button_home_teoria.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_teoria))
        self.button_menu_quiz.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_quiz))

    def profesor(self):
        uic.loadUi("ui/diseno_profesor.ui", self)  #P1: mostraba la GUI  disenofinal.ui
        self.stackedWidget.setCurrentWidget(self.page_home)
        self.label_userName.setText(self.v_usuarioN)
        self.label_userRole.setText(self.v_rolN)
        self.button_menu_home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_home))
        self.button_menu_teoria.clicked.connect(self.Abrir_Modulo_Teoria)
        self.button_menu_practicas.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_practicas))
        self.button_menu_quiz.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_quiz))
        self.button_menu_profesor.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_profesor))
        self.button_menu_cerrar_sesion.clicked.connect(self.cerrarSesion)
        
        self.button_home_teoria.clicked.connect(self.Abrir_Modulo_Teoria)
        self.button_home_practicas.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_practicas))
        self.button_home_quiz.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_quiz))
        
        #-----------Grabar y reproducir audio-----------------------
        self.button_profesor_subir_audio.clicked.connect(self.grabar_profesor)
        #-----------Especificar audio y ruta a reproductir
        self.button_practicas_play.clicked.connect(self.Reproducir_Audio)

        self.button_profesor_play.clicked.connect(self.Reproducir_Audio_partitura)
        #----------- Carga PDF
        self.button_profesor_subir_pdf.clicked.connect(self.Cargar_PDF)
        #----------- comparar
        self.button_compare.clicked.connect(self.prueba_compare)
        self.id_ruta=0
    
    #----------- Modulos ---------------------------------
    def Abrir_Modulo_Teoria(self):
            self.stackedWidget.setCurrentWidget(self.page_teoria)
            self.stackedWidget_2.setCurrentWidget(self.materia_profesor)
            materias = materiaFindAll()
            self.v_table = self.table_temas
            self.v_table.clearContents()
            self.llenarDatosTable(materias)
            self.input_materias_search.setPlaceholderText("Buscar...")
            self.input_materias_search.textChanged.connect(self.searchTable)

    def Abrir_Modulo_Sesiones(self):
        sender_button = self.sender().text()
        if sender_button == "Regresar":
            sender_button = str(self.v_id_materia)

        if sender_button != "Regresar":
            try:
                self.v_id_materia = int(sender_button)
            except:
                self.v_id_materia = -1
                self.mostrarAlerta("Error","Incorrecta celda seleccionada","Por favor seleccione solo el código")
        
            if self.v_id_materia != 0 and self.v_id_materia != -1:
                self.stackedWidget_2.setCurrentWidget(self.sesiones_profesor)
                sesiones = sesionFindAll(self.v_id_materia)
                self.v_table = self.table_sesiones
                self.v_table.clearContents()
                self.llenarDatosTable(sesiones)
                self.input_sesiones_search.setPlaceholderText("Buscar...")
                self.input_sesiones_search.textChanged.connect(self.searchTable)
                self.button_sesiones_crear.clicked.connect(functools.partial(self.crearForm))
                self.button_sesiones_regresar.clicked.connect(functools.partial(self.Abrir_Modulo_Teoria))
            
            elif self.v_id_materia == -1:
                self.v_table.clearContents()
                self.Abrir_Modulo_Teoria()
    
    def Abrir_Modulo_Actividades(self):
        sender_button = self.sender().text()
        if sender_button == "Regresar":
            sender_button = str(self.v_id_sesion)
            
        if sender_button != "Regresar":
            try:
                self.v_id_sesion = int(sender_button)
            except:
                self.v_id_sesion = -1
                self.mostrarAlerta("Error","Incorrecta celda seleccionada","Por favor seleccione solo el código")
        
            if self.v_id_sesion != 0 and self.v_id_sesion != -1:
                self.stackedWidget_2.setCurrentWidget(self.actividades_profesor)
                actividades = actividadFindAll(self.v_id_sesion)
                self.v_table = self.table_actividades
                self.llenarDatosTable(actividades)
                self.input_actividades_search.setPlaceholderText("Buscar...")
                self.input_actividades_search.textChanged.connect(self.searchTable)
                self.button_actividades_crear.clicked.connect(functools.partial(self.crearForm))
                self.button_actividades_regresar.clicked.connect(functools.partial(self.Abrir_Modulo_Sesiones))
            
            elif self.v_id_sesion == -1:
                self.v_table.clearContents()
                self.Abrir_Modulo_Sesiones()

    def Abrir_Modulo_Material_Actividad(self):
        sender_button = self.sender().text()
        if sender_button == "Regresar":
            sender_button = str(self.v_id_actividad)

        if sender_button != "Regresar":
            try:
                self.v_id_actividad = int(sender_button)
            except:
                self.v_id_actividad = -1
                self.mostrarAlerta("Error","Incorrecta celda seleccionada","Por favor seleccione solo el código")
        
            if self.v_id_actividad != 0 and self.v_id_actividad != -1:
                self.stackedWidget_2.setCurrentWidget(self.material_actividad_profesor)
                self.v_table = "table_material_actividad"
                material_actividades = actividadFindAll(self.v_id_actividad)
            elif self.v_id_actividad == -1:
                self.v_table.clearContents()
                self.Abrir_Modulo_Actividades()
            
            self.button_material_actividades_crear.clicked.connect(functools.partial(self.Cargar_materialxActividad))
            self.button_material_actividad_regresar.clicked.connect(functools.partial(self.Abrir_Modulo_Actividades))
            self.llenarMaterial(material_actividades)

    #----------- DISEÑAR MATERIAL ACTIVIDAD ---------------------------------
    def llenarMaterial(self, datos):
        scroll = self.scrollArea_3
        widget = QWidget()
        vbox = QVBoxLayout()
        scroll.setGeometry(100,60,700,530)
        scroll.setWidgetResizable(True)

        for row_number, row_data in enumerate(datos):            
            datos_material = materialByActividad(datos[row_number][0])
            tit = str(row_number+1)
            title = QLabel("Actividad "+tit)
            title.setScaledContents(True)
            title.setWordWrap(True)
            vbox.addWidget(title)

            descripcion = QLabel(datos[row_number][5])
            descripcion.setScaledContents(True)
            descripcion.setWordWrap(True)
            vbox.addWidget(descripcion)

            for r, r_data in enumerate(datos_material):
                try:
                    tipo_material = tipoArchivo(datos_material[r][1])
                except:
                    tipo_material = ""
                
                grid_2 = QGridLayout()
                grid_2.setHorizontalSpacing(6)
                #Horizontal spacer
                space = QSpacerItem(40, 20, QSizePolicy.Expanding)
                count_items = 0
                
                
                if tipo_material != "" and tipo_material[0][1] == "Imagen":
                    pixmap = QPixmap(datos_material[r][2])
                    image = QLabel()
                    image.setPixmap(pixmap)
                    image.setMaximumHeight(200)
                    image.setMaximumWidth(600)
                    image.setScaledContents(True)
                    grid_2.addWidget(image, count_items, 0)

                    #boton eliminar
                    btn = QPushButton(str(datos_material[r][0]), self)
                    btn.setObjectName(str(datos_material[r][0]))
                    btn.clicked.connect(functools.partial(self.eliminar))
                    btn.setStyleSheet("background-color: rgb(195, 44, 45); color: rgb(195, 44, 45); font-size: 1px; padding: 5px")
                    btn.setIcon(QIcon('src/icons/icon_eliminar.png'))
                    btn.setIconSize(QSize(30, 30)) 
                    btn.show()
                    grid_2.addWidget(btn, count_items, 1)
                    grid_2.addItem(space, count_items, 2)
                    count_items += 1
                    
                if tipo_material != "" and tipo_material[0][1] == "Audio":
                    btn_audio = QPushButton(str(datos_material[r][0]), self)
                    btn_audio.setObjectName(str(datos_material[r][0]))
                    btn_audio.clicked.connect(lambda: self.Reproducir_Audio_Material())
                    btn_audio.setStyleSheet("background-color: white; color: white; font-size: 1px;")
                    btn_audio.setIcon(QIcon('src/icons/icon_play.png'))
                    btn_audio.setIconSize(QSize(40, 40)) 
                    btn_audio.show()
                    grid_2.addWidget(btn_audio, count_items, 0)
                    #boton eliminar
                    btn = QPushButton(str(datos_material[r][0]), self)
                    btn.setObjectName(str(datos_material[r][0]))
                    btn.clicked.connect(functools.partial(self.eliminar))
                    btn.setStyleSheet("background-color: rgb(195, 44, 45); color: rgb(195, 44, 45); font-size: 1px; padding: 5px")
                    btn.setIcon(QIcon('src/icons/icon_eliminar.png'))
                    btn.setIconSize(QSize(30, 30)) 
                    btn.show()
                    grid_2.addWidget(btn, count_items, 1)
                    grid_2.addItem(space, count_items, 2)
            
                vbox.addLayout(grid_2)

        widget.setLayout(vbox)
        #Scroll Area Properties
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        self.show()

    #----------- FUNCIONES TABLAS ---------------------------------
    def searchTable(self, s):
        self.v_table.setCurrentItem(None)
        
        if not s: 
            return

        matching_items = self.v_table.findItems(s, Qt.MatchContains)
        if matching_items:
            # We have found something.
            item = matching_items[0]  # Take the first.
            self.v_table.setCurrentItem(item)
    
    def llenarDatosTable(self, datos):
        self.v_table.setRowCount(0)
        tname = self.v_table.objectName()
        
        for row_number, row_data in enumerate(datos):
            self.v_table.insertRow(row_number)
            self.v_table.setItem(row_number, 0, QtWidgets.QTableWidgetItem(row_data[1]))

            #Boton ver
            btn_ver = QPushButton(str(row_data[0]), self)
            btn_ver.setObjectName(str(row_data[0]))
            btn_ver.setStyleSheet("background-color: white; color: white; font-size: 1px;")
            btn_ver.setIcon(QIcon('src/icons/icon_ver.png'))
            btn_ver.setIconSize(QSize(30, 30)) 

            #Boton editar
            btn_editar = QPushButton(str(row_data[0]), self)
            btn_editar.setObjectName(str(row_data[0]))
            btn_editar.setStyleSheet("background-color: white; color: white; font-size: 1px;")
            btn_editar.setIcon(QIcon('src/icons/icon_editar.png'))
            btn_editar.setIconSize(QSize(30, 30)) 

            #Boton eliminar
            btn_eliminar = QPushButton(str(row_data[0]), self)
            btn_eliminar.setObjectName(str(row_data[0]))
            btn_eliminar.setStyleSheet("background-color: white; color: white; font-size: 1px;")
            btn_eliminar.setIcon(QIcon('src/icons/icon_eliminar.png'))
            btn_eliminar.setIconSize(QSize(30, 30)) 

            if tname == "table_temas":
                btn_ver.clicked.connect(functools.partial(self.Abrir_Modulo_Sesiones))
            elif tname == "table_sesiones":
                btn_ver.clicked.connect(functools.partial(self.Abrir_Modulo_Actividades))
                btn_editar.clicked.connect(functools.partial(self.editarForm))
            elif tname == "table_actividades":
                n_act = str(row_number+1)
                n_act = "Actividad "+n_act
                self.v_table.setItem(row_number, 0, QtWidgets.QTableWidgetItem(n_act))
                btn_ver.clicked.connect(functools.partial(self.Abrir_Modulo_Material_Actividad))
                btn_editar.clicked.connect(functools.partial(self.editarForm))
            
            btn_ver.show()
            self.v_table.setCellWidget(row_number, 1, btn_ver)

            if tname != "table_temas":
                btn_editar.show()
                btn_eliminar.show()
                self.v_table.setCellWidget(row_number, 2, btn_editar)
                self.v_table.setCellWidget(row_number, 3, btn_eliminar)

    #----------- FUNCIONES CRUD ---------------------------------
    def guardarForm(self, datos):
        print(datos)
        if datos[0] == "insert_sesiones":
            insertSesiones(datos[1],datos[2], datos[3])
            print("insertadad sesion")
        
        if datos[0] == "update_sesiones":
            updateSesiones(datos[1],datos[2], datos[3])
            print("actualizada sesion")
        
        if datos[0] == "insert_actividades":
            tipoAct = findTipoActividad()
            for r, dat in enumerate(tipoAct):
                #selecciona el id de acuerdo al texto
                if dat[1] == datos[2]:
                    datos[2] = dat[0]
            
            insertar_actividad(datos[1], datos[2], datos[3], datos[4], datos[5])
            print("insertada actividad")
        
        if datos[0] == "update_actividades":
            tipoAct = findTipoActividad()
            for r, dat in enumerate(tipoAct):
                #selecciona el id de acuerdo al texto
                if dat[1] == datos[2]:
                    datos[2] = dat[0]

            actualizar_actividad(datos[1], datos[2], datos[3])
            print("Actualizada actividad")
            
        #datos = [] #vacias datos
    
    def editarForm(self):
        id = int(self.sender().text())
        datos = []
        if self.v_table.objectName() == "table_sesiones":
            sender = "sesion"
            datos = sesionFindId(id)
        
        if self.v_table.objectName() == "table_actividades":
            sender = "actividad"
            datos = actividadFindId(id)
        
        self.form("update", sender, datos[0])
    
    def eliminar(self):
        import os
        id = int(self.sender().text())
        datos = []
        print("id elim",id)
        
        if self.v_table == "table_material_actividad":
            datos = materialById(id)
        
            if datos != []:
                deleteMaterial(datos[0][0])
            
            if os.path.exists(datos[0][2]):
                os.remove(datos[0][2])
            else:
                print("The file does not exist")
                
    
    def crearForm(self):
        if self.sender().text() == "Crear una nueva sesion":
            sender = "sesion"
        elif self.sender().text() == "Crear una nueva actividad":
            sender = "actividad"
        
        #self.sender() = ""
        self.form("insert", sender, 0)

    #----------- DISEÑAR FORMULARIO ---------------------------------
    def form(self, tipo, sender, datos):
        #print("tipo form",tipo, "| datos", datos[1])
        self.stackedWidget_2.setCurrentWidget(self.form_crear)
        scroll = self.scrollArea_form_crear
        widget = QWidget()
        vbox = QVBoxLayout()
        scroll.setWidgetResizable(True)
        grid = QGridLayout()
        grid.setHorizontalSpacing(1)
        #button guardar
        btn_guardar = QPushButton("Guardar", self)

        if sender == "sesion":
            scroll.setGeometry(230,80,400,200)
            datos = datos   #para evitar error de lista "datos" fuera de rango
            self.button_form_crear_regresar.clicked.connect(functools.partial(self.Abrir_Modulo_Sesiones))

            #Label nombre
            self.title_1 = QLabel("Nombre de la sesion")
            self.title_1.setScaledContents(True)
            self.title_1.setWordWrap(True)
            self.title_1.setFont(QFont('Anton', 10, QFont.Bold))

            #Input nombre sesion
            self.input_1 = QLineEdit(self)
            self.input_1.setObjectName("input_1")

            #Label corte
            self.title_2 = QLabel("Corte")
            self.title_2.setScaledContents(True)
            self.title_2.setWordWrap(True)
            self.title_2.setFont(QFont('Anton', 10, QFont.Bold))

            #Select corte
            self.comboBox = QComboBox(self)
            self.comboBox.setObjectName(("comboBox"))
            corte = ["1", "2", "3"]
            
            if tipo == "insert":
                self.label_form_crear_title.setText("Formulario Crear Sesión")
                tabla = "insert_sesiones"
                #Select corte
                self.comboBox.addItems(corte)
                #button guardar
                btn_guardar.clicked.connect(lambda: self.guardarForm([tabla, self.input_1.text(), self.v_id_materia, int(self.comboBox.currentText())]))
                
            elif tipo == "update":
                self.label_form_crear_title.setText("Formulario Editar Sesión")
                tabla = "update_sesiones"
                #Input nombre sesion
                self.input_1.setText(datos[1])
                #ComboBox corte
                print(datos)
                self.comboBox.addItem(str(datos[3]))
                corte.remove(str(datos[3]))     #remueve el item de la bd para evitar duplicados
                self.comboBox.addItems(corte)
                #button guardar
                btn_guardar.clicked.connect(lambda: self.guardarForm([tabla, datos[0], self.input_1.text(), self.comboBox.currentText()]))

            grid.addWidget(self.title_1, 0, 0)
            grid.addWidget(self.input_1, 1, 0)
            grid.addWidget(self.title_2, 2, 0)
            grid.addWidget(self.comboBox, 3, 0)
        
        if sender == "actividad":
            scroll.setGeometry(230,80,400,300)
            datos = datos   #para evitar error de lista "datos" fuera de rango
            self.button_form_crear_regresar.clicked.connect(functools.partial(self.Abrir_Modulo_Actividades))
            tipoAct = findTipoActividad()

            #label actividad
            self.title_1 = QLabel("Tipo de actividad")
            self.title_1.setScaledContents(True)
            self.title_1.setWordWrap(True)
            self.title_1.setFont(QFont('Anton', 10, QFont.Bold))

            #ComboBox tipo actividad
            self.comboBox = QComboBox(self)
            self.comboBox.setObjectName(("comboBox"))

            #label descripcion
            self.title_2 = QLabel("Descripción de la actividad")
            self.title_2.setScaledContents(True)
            self.title_2.setWordWrap(True)
            self.title_2.setFont(QFont('Anton', 10, QFont.Bold))

            #Input descripcion
            self.input_1 = QPlainTextEdit(self)
            self.input_1.setObjectName("input_1")
            #self.input_1.resize(50,50)
            self.input_1.setGeometry(5,5,40,50)


            if tipo == "insert":
                self.label_form_crear_title.setText("Formulario Crear Actividad")
                tabla = "insert_actividades"
                #ComboBox tipo actividad
                for r, dat in enumerate(tipoAct):
                    self.comboBox.addItem(dat[1])

                #button guardar
                btn_guardar.clicked.connect(lambda: self.guardarForm([tabla, self.v_id_sesion, self.comboBox.currentText(), self.v_id_materia, self.v_id_usuario, self.input_1.text()]))
            
            elif tipo == "update":
                self.label_form_crear_title.setText("Formulario Editar Actividad")
                tabla = "update_actividades"
                #ComboBox tipo actividad
                for c_n, dat in enumerate(tipoAct):
                    if dat[0] == datos[2]:      #valida id tablas(actividad => tipo actividad)
                        tipo_activ = dat[1]
                        self.comboBox.addItem(tipo_activ)
                        tipoAct.remove(dat)     #remueve el item de la bd para evitar duplicados
                        break

                for r, dat in enumerate(tipoAct):
                    self.comboBox.addItem(dat[1])
                
                #Input descripcion
                self.input_1.insertPlainText(datos[5])

                #button guardar
                btn_guardar.clicked.connect(lambda: self.guardarForm([tabla, datos[0], self.comboBox.currentText(), self.input_1.text()]))
                
            grid.addWidget(self.title_1, 0, 0)
            grid.addWidget(self.comboBox, 1, 0)
            grid.addWidget(self.title_2, 2, 0)
            grid.addWidget(self.input_1, 3, 0)
            
        btn_guardar.setGeometry(5,5,75,25)
        btn_guardar.setParent(self.frame_button_crear)
        btn_guardar.show()
        vbox.addLayout(grid)
        widget.setLayout(vbox)
        #Scroll Area Properties
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        self.show()

    
        

    def button(self, h):
        sender_button = self.sender().text()
        print(sender_button)
        print(h)

    def Abrir_Modulo_Practica(self):
        print("practica")                    
    def Abrir_Modulo_Quiz(self):
        print("quiz") 
    def prueba_compare(self):
        comparacion_practica(self)
    def grabar_estudiante(self):
        
        if (self.v_rolN=='Estudiante'):
            termino=self.clic()
            if (termino==False):
                self.id_ruta=Grabar_Audio(self,self.v_rolN)
        else:
            print("NO ES ESTUDIANTE ")
            
    def grabar_profesor(self):
        if (self.v_rolN=='Profesor'):
            termino=self.clic()
            if (termino==False):
                self.id_ruta=Grabar_Audio(self,self.v_rolN)
            else:
                print("NO ES PROFESOR ")
    
    def actualizar_examen(self):
        #DEBE REBIRI ID EXAMEN
        #DEBE REcibir campo texto_descripcion y ruta_imagen descripcion de examen
        #DEBE REBIRI UNA LISTA CON LAS RESPUESTAS DE SELECCION MULTIPLE
        self.v_id_examen=1
        print(self.v_id_sesion)
        print(self.v_id_examen)
        id=1
        descripcion_examen='Representadas por medio de unos signos que se escriben en las líneas y espacios del pentagrama. Cada nota representa un sonido musical Marque la nota es la que se marca en color ROJO y la clave musical del pentagrama'
        ruta='src/image_preguntas/pregunta1.png'
        lista_preguntas_recep=[(1,'Nota Si y Clave Fa',1,'f'),(2,'Nota Sol y Clave Sol',1,'v'),(3,'Nota Fa y Clave Sol',1,'f'),(4,'Nota Re y Clave Fa',1,'f')]
        actualizar_preguntas(id,descripcion_examen,ruta,lista_preguntas_recep)

        return "editado"
    
    def actualizar_acti(self):
        actualizar_actividad(1)
        return "actualizado"
        #src/audio/audio_de_profesor/audio_profesor.wav
    
    def mostrarAlerta(self, title, text, descripcion):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setInformativeText(descripcion)
        msg.exec_()
        
    #----------- FUNCIONES ARCHIVOS ---------------------------------
    def Cargar_PDF(self):
        import easygui as eg
        from PIL import Image
        import shutil

        # Copia el archivo desde la ubicación actual a la
        # carpeta "Documentos".
        
        extension = ["*.pdf","*.jpg","*.png"]
        partitura_Pdf = eg.fileopenbox(msg="Abrir archivo",
                         title="Control: fileopenbox",
                         default='',
                         filetypes=extension)
        
        shutil.copyfile(partitura_Pdf, "src/pdf/pdf_profesor/partitura.pdf")
        rta=converter_pdf_to_png()
        print(rta)

    def Cargar_materialxActividad(self):
        import easygui as eg
        from PIL import Image
        import shutil
        import os.path

        # Copia el archivo desde la ubicación actual a la
        # carpeta "Documentos".
        id_act = str(self.v_id_actividad)
        file_path='src/material_actividad/'            
        file_save=f'archivo_actividad_'+id_act

        eextension = ["*.pdf","*.wav","*.png","*.jpg"]
        
        archivo = eg.fileopenbox(msg="Abrir archivo",
                         title="Control: fileopenbox",
                         default='',
                         filetypes=eextension)
        nombre, extension = os.path.splitext(archivo)         
          
        id_extension=0

        if extension == ".pdf": 
            id_extension = 2
            nameArchivo = "_pdf"
        if extension == ".wav": 
            id_extension = 3
            nameArchivo = "_audio"
        if extension == ".png" or extension == ".jpg" : 
            id_extension = 1
            nameArchivo = "_imagen"
        file_save=f'{file_save}{nameArchivo}'
        
        #TIPO MATERIAL - RUTA - DESCRIPCION TXT - SESION - ID DE USUARIO - ACTIVIDAD
        rta=existematerial(file_path+file_save+extension)
    
        i=0
        if rta==True:
            while rta==True:
                separador = "_"
                file_save=f'{file_save}{nameArchivo}{separador}{i}'
                rta=existematerial(file_path+file_save+extension) 
                i=i+1
        if rta==False:
        #RUTA - ID DE USUARIO
            insertar_materialXactividad(id_extension,file_path+file_save+extension,self.v_id_sesion,self.v_id_usuario,self.v_id_actividad)
            print("insertado material")
        
        shutil.copyfile(archivo, file_path+file_save+extension)

    def showPartitura(self):
        from asyncio import subprocess
        import subprocess
        #path = 'src\pdf\tareas.pdf'
        path = 'tareas.pdf'
        subprocess.Popen([path], shell=True)
        print("open partiture...")


    #----------- FUNCIONES AUDIO ---------------------------------
    def clic(self):
        from Metronome.main import main
        rta=main()
        return rta

    def Reproducir_Audio_Material(self):
        #pip uninstall playsound
        #pip install playsound==1.2.2
        from playsound import playsound  
        #Definir Path de lectura (RUTA)
        r_button = int(self.sender().text())
        ruta = materialById(r_button)
        print("Reproduciendo...")
        playsound(ruta[0][2])
        print("Finalizado.")

    def Reproducir_Audio(self):
        #pip uninstall playsound
        #pip install playsound==1.2.2
        from playsound import playsound  
        #Definir Path de lectura (RUTA)
        print("Reproduciendo...")
        playsound('src/audio/compare/profesor/output_profesor.wav')
        print("Finalizado.")

    def Reproducir_Audio_partitura(self):
        #pip uninstall playsound
        #pip install playsound==1.2.2
        from playsound import playsound  
        #Definir Path de lectura (RUTA)
        print("Reproduciendo...")
        playsound('src/audio/compare/profesor/output_profesor.wav')
        print("Finalizado.")

    def xportMidi(self):
        file_in = "src/audio/audio_voz_natural.wav"
        file_out = "src/export_midi/audio_piano_midi.mid"
        audio_data, srate = librosa.load(file_in, sr=None)
        midi = wave_to_midi(audio_data, srate=srate)
        with open (file_out, 'wb') as file:
            midi.writeFile(file)
        print("Done export file MIDI")

    def stop(self):
        quit()

    def Grabar_Audio(self,rol):
        import sounddevice as sd 
        from scipy.io.wavfile import write 
        import wavio as wv  
        print('Grabando...')       
        frequency = 44400        
        duration = 5 
        recording = sd.rec(int(duration * frequency), 
                        samplerate = frequency, channels = 1)         
        sd.wait()         
        #write("recording0.wav", frequency, recording)  
        #Graba en sonido monofonico, para cambiar a stereo va con channels = 2       
        #definir RUTA de guardado
        file_save='' 
        file_path=''
        id_ruta=0
        if (self.v_rolN == 'Estudiante'):
            file_save='voz_solfeo.wav' 
            file_path='src/audio/audio_de_estudiante/'
            rta=existeEvidencia(file_path+file_save)
            print(rta)
            i=0
            if rta==True:
                while rta==True:
                    file_save=f'voz_solfeo{i}.wav' 
                    rta=existeEvidencia(file_path+file_save) 
                    i=i+1
            print(rta)                               
            if rta==False:
            #RUTA - ID DE USUARIO
                id_ruta=insertar_evidencia(file_path+file_save,self.v_id_usuario)
            
        elif (self.v_rolN == 'Profesor'):
            file_save='audio_profesor.wav' 
            file_path='src/audio/audio_de_profesor/'            
            #TIPO MATERIAL - RUTA - DESCRIPCION TXT - SESION - ID DE USUARIO - ACTIVIDAD
            rta=existematerial(file_path+file_save)
            print(rta)
            i=0
            if rta==True:
                while rta==True:
                    file_save=f'audio_profesor{i}.wav' 
                    rta=existematerial(file_path+file_save) 
                    i=i+1
            print(rta)                               
            if rta==False:
            #RUTA - ID DE USUARIO
                id_ruta=insertar_materialXactividad(3,file_path+file_save,2,self.v_id_usuario,1)
        print(file_path+file_save)
        wv.write(file_path+file_save, recording, frequency, sampwidth=2)
        Convertir_Audio_A_MIDI(file_path+file_save,self.v_rolN)
        print('Finalizado con exito')  
        return id_ruta     

    def Convertir_Audio_A_MIDI(file_in,rol):
        import librosa
        from sound_to_midi.monophonic import wave_to_midi
        print("Starting...")
        #file_in = "Basepiano.wav"
        file_out = ""
        if (rol == 'Estudiante'):
            file_out = "src/export_midi/estudiante/audio_estudiante.mid"
        elif (rol == 'Profesor'):
            file_out = "src/export_midi/profesor/midi_partiture.mid"
        
        audio_data, srate = librosa.load(file_in, sr=None)
        print("Audio file loaded!")
        midi = wave_to_midi(audio_data, srate=srate)
        print("Conversion finished!")
        with open (file_out, 'wb') as file:
            midi.writeFile(file)
        print("Done. Exiting!")

        if (rol == 'Estudiante'):
            Midi_to_piano_Estudiante(file_out)
        elif (rol == 'Profesor'):
            Midi_to_piano_Profesor(file_out)
        

    def converter_pdf_to_png():
        
        import fitz
        file_path = "src/pdf/pdf_profesor/partitura.pdf"
        
        zoom = 4  # zoom factor
        # PDF Page is converted into a whole picture 1056*816 and then for each picture a screenshot is taken.
        # zoom = 1.33333333 -----> Image size = 1056*816
        # zoom = 2 ---> 2 * Default Resolution (text is clear, image text is hard to read)    = filesize small / Image size = 1584*1224
        # zoom = 4 ---> 4 * Default Resolution (text is clear, image text is barely readable) = filesize large
        # zoom = 8 ---> 8 * Default Resolution (text is clear, image text is readable) = filesize large
        magnify = fitz.Matrix(zoom, zoom)  # magnifies in x, resp. y direction
        doc = fitz.open(file_path)  # open document
       
        imagen_png=''
        for page in doc:
            pix = page.get_pixmap(matrix=magnify)  # render page to an image
            pix.save(f"src/partitureResources/page-{page.number}.jpg")
            imagen_png=f"src/partitureResources/page-{page.number}.jpg"
            Convertir_PDF_to_MIDI(imagen_png)
           
        #Se pasa la ruta del archivo png generado y se envia para convertir a midi
        return "generó midi"

    def comparacion_practica(self):
        Audio_base='output_profesor.wav'
        Audio_estud='output_estudiante.wav'        
        porcentaje=comparacion_wav(Audio_base,Audio_estud)
        print(porcentaje, porcentaje >= 0.0)
        porcentaje = int(100-(porcentaje/1000))
        nota=0
        #porcentaje=str(porcentaje)+'%'
        if(porcentaje < 0):
            porcentaje = '0%'
            
        else:
            porcentaje = str(porcentaje)
            porcentaje = porcentaje +'%'
        self.porcentaje.setText(porcentaje)
        print(porcentaje)

        #Guardar calificación con evidencia a la actividad
        insertarNota(self.v_id_usuario,1,porcentaje,1,self.id_ruta)
    
    def Convertir_PDF_to_MIDI(partitura):
            filepath=partitureConversion.main.run(partitura)
            print ("Generó MIDI")
            Midi_to_piano_Profesor(filepath)

    def Midi_to_piano_Profesor(ruta_midi_to_piano):
        import  midi_to_wav
        from mido import MidiFile
        #ruta_midi_to_piano='src/export_midi/profesor/midi_partiture.mid'
        file_output='output_profesor.wav'
        rol='Profesor'
        rta=midi_to_wav.Ejemplo.run(ruta_midi_to_piano,file_output,rol) 
        print(rta)

    def Midi_to_piano_Estudiante(ruta_midi_to_piano):
        import  midi_to_wav
        from mido import MidiFile
        #ruta_midi_to_piano='src/export_midi/estudiante/audio_piano_midi.mid'
        rol='Estudiante'
        file_output='output_estudiante.wav'
        rta=midi_to_wav.Ejemplo.run(ruta_midi_to_piano,file_output,rol) 
        print(rta) 

def run():
    print("app running")
    app = QApplication(sys.argv)
    programa = Ventana()
    programa.show()
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':    
    run()
