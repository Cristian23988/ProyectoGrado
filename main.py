from ctypes import pointer
import sys
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QComboBox, QRadioButton, QCheckBox, QLabel, QPlainTextEdit, QFrame, QGridLayout, QPushButton, QScrollArea, QApplication, QSpacerItem,
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
from conexion.user import findLogin
from conexion.materia import findByIdUsuario as materiaFindAll
from conexion.sesion import findByMateria as sesionFindAll
from conexion.sesion import findById as sesionFindId
from conexion.sesion import insert as insertSesiones
from conexion.sesion import update as updateSesiones
from conexion.sesion import deleteById as deleteSesionesId
from conexion.actividad import findBySesion as actividadFindAll
from conexion.actividad import update as actualizar_actividad
from conexion.actividad import insert as insertar_actividad
from conexion.actividad import findById as actividadFindId
from conexion.actividad import findTipoActividades as findTipoActividad
from conexion.actividad import deleteById as deleteActiById
from conexion.actividad import GetActividadXSesionYTipoActividad as findActividadSesionTipo
from conexion.material_actividad import findMaterialByActivity as materialByActividad
from conexion.material_actividad import findById as materialById
from conexion.material_actividad import deleteById as deleteMaterial
from conexion.material_actividad import findByRuta as existematerial
from conexion.material_actividad import insert as guardarMateria_Actividad
from conexion.material_actividad import findMaterialBySesion as findMaterialBySesion
from conexion.preguntas import update as actualizar_preguntas
from conexion.preguntas import findByExameneXActividad as findExamenAct
from conexion.preguntas import insert as insertExamen
from conexion.preguntas import findByRuta as existerutaPregunta
from conexion.tipo_archivo import findById as tipoArchivo
from conexion.material_actividad import insert as insertar_materialXactividad
from conexion.preguntas import update as actualizar_preguntas
from conexion.evidencia_estudiante import insert as insertar_evidencia
from conexion.evidencia_estudiante import findByRuta as existeEvidencia
from conexion.materia_estudiante import findByIdEstudiante as materiaEstudiante
from conexion.notas import insert as insertarNota
from partitureConversion.MIDIUtil.src.midiutil.MidiFile3 import MIDIFile
from Comparacion.compare import comparacion_wav

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
        v_tipo_actividad = 0
        v_id_actividad = 0
        v_respuesta_correcta = -1
        v_respuestas_exam = []

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
        uic.loadUi("ui/diseno_profesor_copy.ui", self)  #P1: mostraba la GUI  disenofinal.ui
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
        #self.button_profesor_subir_audio.clicked.connect(self.iniciargrabar)
        #-----------Especificar audio y ruta a reproductir
        self.button_practicas_play.clicked.connect(self.Reproducir_Audio)

        self.button_profesor_play.clicked.connect(self.Reproducir_Audio_partitura)
        #----------- Carga PDF
        self.button_profesor_subir_pdf.clicked.connect(self.Cargar_PDF)
        #----------- comparar
        self.button_compare.clicked.connect(self.prueba_compare)
        self.id_ruta=0

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
        #self.button_profesor_subir_audio.clicked.connect(self.iniciargrabar)
        #-----------Especificar audio y ruta a reproductir
        self.button_practicas_play.clicked.connect(self.Reproducir_Audio)

        self.button_profesor_play.clicked.connect(self.Reproducir_Audio_partitura)
        #----------- Carga PDF
        self.button_profesor_subir_pdf.clicked.connect(self.Cargar_PDF)
        #----------- comparar
        #self.button_compare.clicked.connect(self.prueba_compare)
        self.id_ruta=0
    
    #----------- Modulos ---------------------------------
    def Abrir_Modulo_Teoria(self):
            self.stackedWidget.setCurrentWidget(self.page_teoria)
            self.stackedWidget_2.setCurrentWidget(self.materia_profesor)
            if self.v_rolN == "Profesor":
                materias = materiaFindAll(self.v_id_usuario)
            elif self.v_rolN == "Estudiante":
                materias = materiaEstudiante(self.v_id_usuario)
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
                if self.v_rolN == "Profesor":
                    self.button_sesiones_crear.clicked.connect(functools.partial(self.crearForm))
                self.button_sesiones_regresar.clicked.connect(functools.partial(self.Abrir_Modulo_Teoria))
            
            elif self.v_id_materia == -1:
                self.v_table.clearContents()
                self.Abrir_Modulo_Teoria()
    
    def Abrir_Modulo_Tipo_Actividades(self):
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
                self.stackedWidget_2.setCurrentWidget(self.tipo_actividades_profesor)
                #actividades = actividadFindAll(self.v_id_sesion)
                self.v_table = "table_tipo_actividades"
                #self.llenarDatosTable(actividades)
                #self.input_actividades_search.setPlaceholderText("Buscar...")
                #self.input_actividades_search.textChanged.connect(self.searchTable)
                self.button_tipo_actividad_1.clicked.connect(lambda: self.Abrir_Modulo_Actividades(self.v_id_sesion, 3))
                self.button_tipo_actividad_2.clicked.connect(lambda: self.Abrir_Modulo_Actividades(self.v_id_sesion, 2))
                self.button_tipo_actividad_3.clicked.connect(lambda: self.Abrir_Modulo_Actividades(self.v_id_sesion, 4))
                self.button_tipo_actividad_4.clicked.connect(lambda: self.Abrir_Modulo_Actividades(self.v_id_sesion, 1))
                self.button_tipo_actividades_regresar.clicked.connect(functools.partial(self.Abrir_Modulo_Sesiones))
            
            elif self.v_id_sesion == -1:
                self.v_table.clearContents()
                self.Abrir_Modulo_Sesiones()
    
    def Abrir_Modulo_Actividades(self, id, tipo):
        if id != 0 and tipo != 0:
            self.v_tipo_actividad = tipo
            sender_button = id
        else:
            sender_button = "Regresar"
            
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
                actividades = findActividadSesionTipo(self.v_id_sesion, self.v_tipo_actividad)
                self.v_table = self.table_actividades
                self.llenarDatosTable(actividades)
                self.input_actividades_search.setPlaceholderText("Buscar...")
                self.input_actividades_search.textChanged.connect(self.searchTable)
                if self.v_rolN == "Profesor":
                    self.button_actividades_crear.clicked.connect(functools.partial(self.crearForm))
                self.button_actividades_regresar.clicked.connect(functools.partial(self.Abrir_Modulo_Tipo_Actividades))
            
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
                material_actividades = materialByActividad(self.v_id_actividad)
            elif self.v_id_actividad == -1:
                #self.v_table.clearContents()
                self.Abrir_Modulo_Actividades(self.v_id_sesion, self.v_tipo_actividad)
            
            if self.v_tipo_actividad == 3:
                self.v_table = "table_material_actividad"
                #self.button_material_actividades_crear.clicked.connect(functools.partial(self.Cargar_materialxActividad))
            elif self.v_tipo_actividad == 4:
                self.v_table = "table_quiz_teorico"
                #self.button_material_actividades_crear.clicked.connect(functools.partial(self.crearForm))
            elif self.v_tipo_actividad == 1:
                self.v_table = "table_quiz_solfeo"
                #self.button_material_actividades_crear.clicked.connect(functools.partial(self.crearForm))
            elif self.v_tipo_actividad == 2:
                print("material_actividades",material_actividades)
                self.v_table = "table_practica"
                ##self.button_material_actividades_crear.clicked.connect(functools.partial(self.crearForm))
            self.button_material_actividad_regresar.clicked.connect(lambda: self.Abrir_Modulo_Actividades(self.v_id_sesion, self.v_tipo_actividad))
            self.llenarMaterial(material_actividades)

    #----------- DISEÑAR MATERIAL ACTIVIDAD ---------------------------------
    def llenarMaterial(self, datos):
        print("self.v_tipo_actividad",self.v_tipo_actividad)
        if self.v_tipo_actividad == 3:
            self.llenarMaterialTeoria(datos)
        elif self.v_tipo_actividad == 4:
            self.llenarMaterialQuiz(datos)
        elif self.v_tipo_actividad == 2:
            self.llenarMaterialTeoria(datos)
        elif self.v_tipo_actividad == 1:
            self.llenarMaterialTeoria(datos)
    
    def llenarMaterialTeoria(self, datos):
        print("llenar material",datos)
        
        datos_material = datos
        scroll = self.scrollArea_3
        widget = QWidget()
        vbox = QVBoxLayout()
        scroll.setGeometry(100,60,700,530)
        scroll.setWidgetResizable(True)
        
        grid_boton = QGridLayout()
        grid_boton.setHorizontalSpacing(6)
        btn = QPushButton("Crear una nueva actividad", self)
        btn.setObjectName("Crear una nueva actividad")
        btn.clicked.connect(functools.partial(self.crearForm))
        btn.setStyleSheet("background-color: rgb(195, 44, 45); color: rgb(195, 44, 45); font-size: 1px; padding: 5px")
        btn.setIcon(QIcon('src/icons/icon_home.png'))
        btn.setIconSize(QSize(30, 30)) 

        btn_grabar = QPushButton("Grabar audio", self)
        btn_grabar.setObjectName("Grabar audio")
        btn_grabar.clicked.connect(lambda: self.iniciargrabar())
        btn_grabar.setStyleSheet("background-color: white; color: black; font-size: 8px;")
        btn_grabar.setIcon(QIcon('src/icons/icon_agregar.png'))
        btn_grabar.setIconSize(QSize(40, 40)) 
        
        btn_comparar = QPushButton("Enviar Audio Grabado", self)
        btn_comparar.setObjectName("Comparar")
        
        btn_comparar.clicked.connect(lambda: self.comparar())
        btn_comparar.setStyleSheet("background-color: white; color: black; font-size: 8px;")
        btn_comparar.setIcon(QIcon('src/icons/icon_agregar.png'))
        btn_comparar.setIconSize(QSize(40, 40)) 
        
        if (self.v_tipo_actividad == 3 or self.v_tipo_actividad == 4) and self.v_rolN != 'Estudiante':
            btn.show()
            grid_boton.addWidget(btn, 0, 0)
        elif self.v_tipo_actividad == 1 or self.v_tipo_actividad == 2:
            btn_grabar.show()
            if self.v_rolN=='Estudiante':
                space_button = QSpacerItem(40, 20, QSizePolicy.Expanding)
                btn_comparar.show()
                grid_boton.addWidget(btn_comparar, 0, 1)
                grid_boton.addWidget(btn_grabar, 0, 0)
                grid_boton.addItem(space_button, 0 ,2)
            else:  
                grid_boton.addWidget(btn_grabar, 0, 0)

        for row_number, row_data in enumerate(datos):            
            datos_material = datos
            tit = str(row_number+1)
            title = QLabel("Material "+tit)

            title.setScaledContents(True)
            title.setWordWrap(True)
            vbox.addWidget(title)

            desc = str(datos[0][5])
            if(self.v_tipo_actividad != 3):
                desc = actividadFindId(datos[0][5])
                desc = desc[0][5]
            descripcion = QLabel(desc)
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
                c_items = 0
                
                if self.v_rolN == "Estudiante" and self.v_tipo_actividad != 3 and self.v_tipo_actividad != 4:
                    Convertir_Audio_A_MIDI(datos[0][2],'Profesor')

                if tipo_material != "" and self.v_rolN == "Profesor":
                    #boton eliminar
                    btn = QPushButton(str(datos_material[r][0]), self)
                    btn.setObjectName(str(datos_material[r][0]))
                    btn.clicked.connect(functools.partial(self.eliminar))
                    btn.setStyleSheet("background-color: rgb(195, 44, 45); color: rgb(195, 44, 45); font-size: 1px; padding: 5px")
                    btn.setIcon(QIcon('src/icons/icon_eliminar.png'))
                    btn.setIconSize(QSize(30, 30)) 
                    btn.show()

                if tipo_material != "" and tipo_material[0][1] == "Imagen":
                    print("siii",datos_material[r][2], self.v_tipo_actividad)
                    if datos_material[r][2] == "" and self.v_tipo_actividad == 2:
                        datos_material[r][2] = "src/images/image_practic.jpg"
                    elif datos_material[r][2] == "":
                        datos_material[r][2] = "src/images/image_quiz.jpg"

                    pixmap = QPixmap(datos_material[r][2])
                    image = QLabel()
                    image.setPixmap(pixmap)
                    image.setMaximumHeight(200)
                    image.setMaximumWidth(600)
                    image.setScaledContents(True)

                    grid_2.addWidget(image, count_items, c_items)
                    c_items += 1
                    if self.v_rolN == "Profesor":
                        grid_2.addWidget(btn, count_items, c_items)
                        c_items += 1
                    grid_2.addItem(space, count_items, c_items)
                    c_items = 0
                    count_items += 1
                
                else:
                    #print("siii",datos_material[r][2], self.v_tipo_actividad)
                    if self.v_tipo_actividad == 2:
                        url_image = "src/images/image_practic.jpg"
                    else:
                        url_image = "src/images/image_quiz.jpg"

                    pixmap = QPixmap(url_image)
                    image = QLabel()
                    image.setPixmap(pixmap)
                    image.setMaximumHeight(200)
                    image.setMaximumWidth(600)
                    image.setScaledContents(True)

                    grid_2.addWidget(image, count_items, c_items)
                    c_items += 1
                    grid_2.addItem(space, count_items, c_items)
                    c_items = 0
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
                    c_items += 1
                    if self.v_rolN == "Profesor":
                        grid_2.addWidget(btn, count_items, c_items)
                        c_items += 1
                    grid_2.addItem(space, count_items, c_items)
                    c_items = 0
                    count_items += 1
                
                if tipo_material != "" and tipo_material[0][1] == "PDF":
                    btn_audio = QPushButton(str(datos_material[r][0]), self)
                    btn_audio.setObjectName(str(datos_material[r][0]))
                    btn_audio.clicked.connect(lambda: self.showPartitura(datos_material[r][2]))
                    btn_audio.setStyleSheet("background-color: white; color: white; font-size: 1px;")
                    btn_audio.setIcon(QIcon('src/icons/icon_play.png'))
                    btn_audio.setIconSize(QSize(40, 40)) 
                    btn_audio.show()

                    grid_2.addWidget(btn_audio, count_items, 0)
                    c_items += 1
                    if self.v_rolN == "Profesor":
                        grid_2.addWidget(btn, count_items, c_items)
                        c_items += 1
                    grid_2.addItem(space, count_items, c_items)
                    c_items = 0
                    count_items += 1
            
                vbox.addLayout(grid_2)
        vbox.addLayout(grid_boton)
        widget.setLayout(vbox)
        #Scroll Area Properties
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        self.show()
    
    def llenarMaterialQuiz(self, datos):
        self.v_respuestas_exam = []
        datos, datos_exam = findExamenAct(self.v_id_actividad, self.v_id_sesion)
        print("llenar material quiz",datos)
        print("llenar material quiz",datos_exam)
        scroll = self.scrollArea_3
        widget = QWidget()
        vbox = QVBoxLayout()
        scroll.setGeometry(100,60,700,530)
        scroll.setWidgetResizable(True)

        grid_boton = QGridLayout()
        grid_boton.setHorizontalSpacing(6)
        btn = QPushButton("Guardar Examen", self)
        btn.setObjectName("Guardar Examen")
        if self.v_rolN == "Estudiante":
            btn.clicked.connect(lambda: self.guardarForm(["Guardar Examen"]))
        else:
            btn.clicked.connect(functools.partial(self.crearForm))
        btn.setStyleSheet("background-color: rgb(195, 44, 45); color: rgb(195, 44, 45); font-size: 1px; padding: 5px")
        btn.setIcon(QIcon('src/icons/icon_home.png'))
        btn.setIconSize(QSize(30, 30))
        btn.show()
        grid_boton.addWidget(btn, 0, 0)
        

        for row_number, row_data in enumerate(datos):
            tit = str(row_number+1)
            title = QLabel("Material Quiz"+tit)

            title.setScaledContents(True)
            title.setWordWrap(True)
            vbox.addWidget(title)

            descripcion = QLabel(row_data[2])
            descripcion.setScaledContents(True)
            descripcion.setWordWrap(True)
            vbox.addWidget(descripcion)

            grid_2 = QGridLayout()
            grid_2.setHorizontalSpacing(6)
            #Horizontal spacer
            space = QSpacerItem(40, 20, QSizePolicy.Expanding)
            count_items = 0
            c_items = 0
            #boton eliminar
            btn = QPushButton(str(row_data[0]), self)
            btn.setObjectName(str(row_data[0]))
            btn.clicked.connect(functools.partial(self.eliminar))
            btn.setStyleSheet("background-color: rgb(195, 44, 45); color: rgb(195, 44, 45); font-size: 1px; padding: 5px")
            btn.setIcon(QIcon('src/icons/icon_eliminar.png'))
            btn.setIconSize(QSize(30, 30)) 

            if row_data[3] != "":
                pixmap = QPixmap(str(row_data[3]))
                image = QLabel()
                image.setPixmap(pixmap)
                image.setMaximumHeight(200)
                image.setMaximumWidth(600)
                image.setScaledContents(True)

                grid_2.addWidget(image, count_items, c_items)
                c_items += 1
                if self.v_rolN == "Profesor":
                    btn.show()
                    grid_2.addWidget(btn, count_items, c_items)
                    c_items += 1
                grid_2.addItem(space, count_items, c_items)
                c_items = 0
                count_items += 1
            
            for r, r_data in enumerate(datos_exam):
                if datos[row_number][0] == r_data[2]:
                    b = QRadioButton(r_data[1], self)
                    b.toggled.connect(lambda: self.button(b, datos[row_number][0]))

                    grid_2.addWidget(b, count_items, 0)
                    c_items += 1
                    if self.v_rolN == "Profesor":
                        #boton eliminar
                        btn_2 = QPushButton(str(r_data[0]), self)
                        btn_2.setObjectName(str(r_data[0]))
                        btn_2.clicked.connect(functools.partial(self.eliminar))
                        btn_2.setStyleSheet("background-color: rgb(195, 44, 45); color: rgb(195, 44, 45); font-size: 1px; padding: 5px")
                        btn_2.setIcon(QIcon('src/icons/icon_eliminar.png'))
                        btn_2.setIconSize(QSize(30, 30)) 
                        btn_2.show()
                        grid_2.addWidget(btn_2, count_items, c_items)
                        c_items += 1
                    grid_2.addItem(space, count_items, c_items)
                    c_items = 0
                    count_items += 1
            vbox.addLayout(grid_2)

        vbox.addLayout(grid_boton)
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
                btn_ver.clicked.connect(functools.partial(self.Abrir_Modulo_Tipo_Actividades))
                if self.v_rolN == "Profesor":
                    btn_editar.clicked.connect(functools.partial(self.editarForm))
                    btn_eliminar.clicked.connect(functools.partial(self.eliminar))
            elif tname == "table_actividades":
                n_act = str(row_number+1)
                n_act = "Actividad "+n_act
                self.v_table.setItem(row_number, 0, QtWidgets.QTableWidgetItem(n_act))
                btn_ver.clicked.connect(functools.partial(self.Abrir_Modulo_Material_Actividad))
                if self.v_rolN == "Profesor":
                    btn_editar.clicked.connect(functools.partial(self.editarForm))                
                    btn_eliminar.clicked.connect(functools.partial(self.eliminar))
            
            btn_ver.show()
            self.v_table.setCellWidget(row_number, 1, btn_ver)

            if tname != "table_temas" and self.v_rolN == "Profesor":
                btn_editar.show()
                btn_eliminar.show()
                self.v_table.setCellWidget(row_number, 2, btn_editar)
                self.v_table.setCellWidget(row_number, 3, btn_eliminar)

    #----------- FUNCIONES CRUD ---------------------------------
    def guardarForm(self, datos):
        import shutil
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
        
        if datos[0] == "Guardar Examen":
            act,examenes = findExamenAct(self.v_id_actividad, self.v_id_sesion)
            # print("countt")
            # print(len(examenes))
            # print(len(self.v_respuestas_exam))
            # print("datttt")
            # print(examenes)
            # print(self.v_respuestas_exam)

            #for r_n, r_d in enumerate():

            rta = self.mostrarAlertaSiNo(f"Insertar Examen","","Seguro que desea insertar examen?")
            if rta==True:
                #insertarNota(datos[1],datos[2],datos[3],datos[4],datos[5])
                pass
            elif rta==False:
                print("No inserta")   

            
        #datos = [] #vacias datos
        if datos[0] == "insert_quiz_teorico":
            if self.v_respuesta_correcta != -1:
                datos[5][self.v_respuesta_correcta-1][1] = 1
            
            rta=self.mostrarAlertaSiNo(f"Insertar Examen","","Seguro que desea insertar examen?")
            if rta==True:
                shutil.copyfile(self.v_archivo_Origen, datos[4])
                insertExamen(datos[1],datos[2],datos[3],datos[4],datos[5])
            elif rta==False:
                print("No inserta")   

    
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
        id = int(self.sender().text())
        datos_sesiones = []
        datos_actividades = []
        datos_material = []
        print("id elim",id)
         
        #DATO CURIOSO NO DEJA BORRAR MATERIAL CON EL .OBJECTNAME PERO SI DATOS DE LAS LISTAS
        #SIN EL OBJECTNAME SI BORRA LAS IMAGENES PERO SE DAÑA CON LOS ITEMS DE LA TABLA
        if self.v_table == "table_material_actividad":
            datos_material = materialById(id)
        
            if datos_material != []:
                deleteMaterial(datos_material[0][0])
                self.borrarArchivosLocal(datos_material[0][2])
        
        elif self.v_table.objectName() == "table_actividades":
            datos_actividades = actividadFindId(id)
            rta=self.mostrarAlertaSiNo(f"Eliminar actividad","","Seguro que desea eliminar esta actividad?")
            if rta==True:
                datos_material = materialByActividad(id)
                deleteActiById(id)
                for row, dat in enumerate(datos_material):
                    self.borrarArchivosLocal(dat[2])
                print("Eliminado")    

            elif rta==False:
                print("No elimina")    
            


            print(datos_actividades)

        elif self.v_table.objectName() == "table_sesiones":
            rta=self.mostrarAlertaSiNo(f"Eliminar Sesión","","Seguro que desea eliminar esta sesión?")
            if rta==True:           
                datos_material = findMaterialBySesion(id) 
                deleteSesionesId(id)
                for row, dat in enumerate(datos_material):
                    self.borrarArchivosLocal(dat[2])
                print("Eliminado")    
            elif rta==False:
                print("No elimina")    
            
    def borrarArchivosLocal(self, rutaArchivo):
        import os
        if os.path.exists(rutaArchivo):
            os.remove(rutaArchivo)
        else:
            print("The file does not exist")
                
    
    def crearForm(self):
        if self.sender().text() == "Crear una nueva sesion":
            sender = "sesion"
        elif self.sender().text() == "Crear una nueva actividad":
            sender = "actividad"
        elif self.v_table == "table_quiz_teorico":
            sender = "quiz_teorico"

        #self.sender() = ""
        self.form("insert", sender, 0)
    
    def isChecked(self):
        print("is checked",self.sender().text())
        self.v_respuesta_correcta = int(self.sender().text())
    
    def button(self, h, t):
        sender_button = self.sender().text()
        self.v_respuestas_exam.append([sender_button, t])
        print("jakfjalsfj")
        print(sender_button)
        print(t)

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
            self.button_form_crear_regresar.clicked.connect(lambda: self.Abrir_Modulo_Actividades(self.v_id_sesion, self.v_tipo_actividad))
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
            self.input_1.setGeometry(5,5,40,50)

            if tipo == "insert":
                
                self.label_form_crear_title.setText("Formulario Crear Actividad")
                tabla = "insert_actividades"
                #ComboBox tipo actividad
                for r, dat in enumerate(tipoAct):
                    self.comboBox.addItem(dat[1])

                #button guardar
                btn_guardar.clicked.connect(lambda: self.guardarForm([tabla, self.v_id_sesion, self.comboBox.currentText(), self.v_id_materia, self.v_id_usuario, self.input_1.toPlainText()]))
            
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
                btn_guardar.clicked.connect(lambda: self.guardarForm([tabla, datos[0], self.comboBox.currentText(), self.input_1.toPlainText()]))
            
                
            grid.addWidget(self.title_1, 0, 0)
            grid.addWidget(self.comboBox, 1, 0)
            grid.addWidget(self.title_2, 2, 0)
            grid.addWidget(self.input_1, 3, 0)
        
        if sender == "quiz_teorico":
            self.v_respuesta_correcta = -1
            self.v_ruta_examen = ""
            scroll.setGeometry(230,80,400,450)
            datos = datos   #para evitar error de lista "datos" fuera de rango
            self.button_form_crear_regresar.clicked.connect(lambda: self.Abrir_Modulo_Actividades(self.v_id_sesion, self.v_tipo_actividad))
            tipoAct = findTipoActividad()

            #label descripcion
            self.title_1 = QLabel("Descripcion del examen")
            self.title_1.setScaledContents(True)
            self.title_1.setWordWrap(True)
            self.title_1.setFont(QFont('Anton', 10, QFont.Bold))

            #label descripcion
            self.title_2 = QLabel("Respuestas")
            self.title_2.setScaledContents(True)
            self.title_2.setWordWrap(True)
            self.title_2.setFont(QFont('Anton', 10, QFont.Bold))

            #label descripcion
            self.title_3 = QLabel("Cargar imagen")
            self.title_3.setScaledContents(True)
            self.title_3.setWordWrap(True)
            self.title_3.setFont(QFont('Anton', 10, QFont.Bold))

            #label actividad
            self.title_4 = QLabel("Respuesta 1")
            self.title_4.setScaledContents(True)
            self.title_4.setWordWrap(True)
            self.title_4.setFont(QFont('Anton', 10, QFont.Bold))
            self.title_5 = QLabel("Respuesta 2")
            self.title_5.setScaledContents(True)
            self.title_5.setWordWrap(True)
            self.title_5.setFont(QFont('Anton', 10, QFont.Bold))
            self.title_6 = QLabel("Respuesta 3")
            self.title_6.setScaledContents(True)
            self.title_6.setWordWrap(True)
            self.title_6.setFont(QFont('Anton', 10, QFont.Bold))
            self.title_7 = QLabel("Respuesta 4")
            self.title_7.setScaledContents(True)
            self.title_7.setWordWrap(True)
            self.title_7.setFont(QFont('Anton', 10, QFont.Bold))
            self.title_8 = QLabel("Respuesta correcta:")
            self.title_8.setScaledContents(True)
            self.title_8.setWordWrap(True)
            self.title_8.setFont(QFont('Anton', 10, QFont.Bold))

            #Input descripcion
            self.input_1 = QPlainTextEdit(self)
            self.input_1.setObjectName("input_1")
            self.input_1.setGeometry(5,5,40,50)

            #Input preguntas
            self.input_2 = QLineEdit(self)
            self.input_2.setObjectName("input_2")
            self.input_2.setGeometry(5,5,40,50)
            self.input_3 = QLineEdit(self)
            self.input_3.setObjectName("input_3")
            self.input_3.setGeometry(5,5,40,50)
            self.input_4 = QLineEdit(self)
            self.input_4.setObjectName("input_4")
            self.input_4.setGeometry(5,5,40,50)
            self.input_5 = QLineEdit(self)
            self.input_5.setObjectName("input_5")
            self.input_5.setGeometry(5,5,40,50)

            #Horizontal spacer
            space = QSpacerItem(40, 20, QSizePolicy.Expanding)

            #imagen
            #self.frame = QFrame(self)
            #self.frame.resize(100,50)
            grid_3 = QGridLayout()
            grid_3.setHorizontalSpacing(6)
            btn_imagen = QPushButton("imagen", self)
            btn_imagen.clicked.connect(self.pathArchivo)
            btn_imagen.setParent(self.frame)
            btn_imagen.show()
            grid_3.addWidget(btn_imagen, 0, 0)
            grid_3.addItem(space,0,1)
            
            grid_2 = QGridLayout()
            grid_2.setHorizontalSpacing(6)

            #checkbox
            x = range(0, 4)
            for n in x:
                b = QRadioButton(str(n+1), self)
                b.objectName()
                b.toggled.connect(self.isChecked)
                grid_2.addWidget(b, 0, n)
            
            grid_2.addItem(space, 0, 5)  

            if tipo == "insert":
                self.label_form_crear_title.setText("Formulario Crear Examen")
                tabla = "insert_quiz_teorico"

                #button guardar
                btn_guardar.clicked.connect(lambda: self.guardarForm([tabla, self.v_id_actividad, self.v_id_sesion, self.input_1.toPlainText(), self.v_ruta_examen, [[self.input_2.text() , 0] , [self.input_3.text(), 0] , [self.input_4.text(), 0] , [self.input_5.text(), 0]]]))
            
            grid.addWidget(self.title_1, 0, 0)
            grid.addWidget(self.input_1, 1, 0)
            grid.addWidget(self.title_2, 2, 0)
            grid.addWidget(self.title_4, 3, 0)
            grid.addWidget(self.input_2, 4, 0)
            grid.addWidget(self.title_5, 5, 0)
            grid.addWidget(self.input_3, 6, 0)
            grid.addWidget(self.title_6, 7, 0)
            grid.addWidget(self.input_4, 8, 0)
            grid.addWidget(self.title_7, 9, 0)
            grid.addWidget(self.input_5, 10, 0)
            grid.addWidget(self.title_8, 11, 0)
            grid.addItem(grid_2, 12, 0)
            grid.addWidget(self.title_3, 13, 0)
            grid.addItem(grid_3, 14, 0)

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

    
        

    def Abrir_Modulo_Practica(self):
        print("practica")                    
    def Abrir_Modulo_Quiz(self):
        print("quiz") 
    def prueba_compare(self):
        comparacion_practica(self)

     
    def iniciargrabar(self):
        
            termino=self.clic()
            if (termino==False):
                self.id_ruta=self.Grabar_Audio()
            
       
         
    
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

    def mostrarAlertaSiNo(self, title, text, descripcion):
            reply=QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',                                                           
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                return True
            else:
                return False
    def comparar(self):
        rta= self.mostrarAlertaSiNo("Enviar audio","","Seguro quiere enviar?")
        if rta==True:
            self.prueba_compare()
        else:
            pass
        
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

    def pathArchivo(self):
        import easygui as eg
        from PIL import Image
        import shutil
        import os.path

        # Copia el archivo desde la ubicación actual a la
        # carpeta "Documentos".
        #id_act = str(self.v_id_examen)
        id_act = "1"
        file_path='src/image_preguntas/'
        file_save=f'archivo_pregunta_'+id_act

        eextension = ["*.png","*.jpg"]
        
        archivo = eg.fileopenbox(msg="Abrir archivo",
                         title="Control: fileopenbox",
                         default='',
                         filetypes=eextension)
        nombre, extension = os.path.splitext(archivo)         
          
        id_extension=0

        if extension == ".png" or extension == ".jpg" : 
            id_extension = 1
            nameArchivo = "_imagen"
        file_save=f'{file_save}{nameArchivo}'
        
        #TIPO MATERIAL - RUTA - DESCRIPCION TXT - SESION - ID DE USUARIO - ACTIVIDAD
        rta=existerutaPregunta(file_path+file_save+extension)
    
        i=0
        if rta==True:
            while rta==True:
                separador = "_"
                file_save=f'{file_save}{nameArchivo}{separador}{i}'
                rta=existerutaPregunta(file_path+file_save+extension) 
                i=i+1
        
        self.v_ruta_examen = file_path+file_save+extension
        self.v_archivo_Origen=archivo
        return file_path+file_save+extension
        #shutil.copyfile(archivo, file_path+file_save+extension)

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

    def showPartitura(self, pdf):
        import webbrowser
        from pathlib import Path
        #rut = 'src/pdf/fire.pdf'
        mypath = Path().absolute()
        path = mypath/pdf
        webbrowser.open_new(path)
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

    def Grabar_Audio(self):
        import sounddevice as sd 
        from scipy.io.wavfile import write 
        import wavio as wv  
        rol=self.v_rolN
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
                id_ruta=insertar_materialXactividad(3,file_path+file_save,self.v_id_sesion,self.v_id_usuario,self.v_id_actividad)
        print(file_path+file_save)
        wv.write(file_path+file_save, recording, frequency, sampwidth=2)
        if self.v_rolN=='Estudiante':
           Convertir_Audio_A_MIDI(file_path+file_save,self.v_rolN)
        print('Finalizado con exito')  
        return id_ruta     

def Convertir_Audio_A_MIDI(file_in,rol):
        print("ruta",file_in)
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
        self.porcentaje_audio.setText(porcentaje)
        print(porcentaje)

        #Guardar calificación con evidencia a la actividad
        insertarNota(self.v_id_usuario,self.v_id_actividad,porcentaje,1,self.id_ruta)
    
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
