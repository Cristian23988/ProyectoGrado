from ctypes import pointer
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QFrame, QGridLayout, QPushButton, QScrollArea, QApplication, QSpacerItem,
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
from conexion.actividad import findBySesion as actividadFindAll
from conexion.material_actividad import findMaterialByActivity as materialByActividad
from conexion.material_actividad import findById as materialById
from conexion.tipo_archivo import findById as tipoArchivo
s = stream.Stream()
        
class Ventana(QMainWindow):
    
    def __init__(self):
        super(Ventana, self).__init__()
        uic.loadUi("ui/login.ui", self)  #P1: mostraba la GUI  disenofinal.ui
        self.button_login.clicked.connect(lambda:self.logIn(self.input_login_correo.text(),self.input_login_contrasena.text()))
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
        #Grabar y reproducir audio-----------------------
        
        self.button_profesor_subir_audio.clicked.connect(self.grabar_profesor)
        #-----------Especificar audio y ruta a reproductir
        self.button_practicas_play.clicked.connect(self.Reproducir_Audio)

        self.button_profesor_play.clicked.connect(self.Reproducir_Audio_partitura)
        #Carga PDF

        #self.button_profesor_subir_pdf.clicked.connect(self.prueba)
        self.button_profesor_subir_pdf.clicked.connect(self.Cargar_PDF)

        self.button_compare.clicked.connect(self.prueba_compare)
        self.id_ruta=0
        
        #self.botonMidi.clicked.connect(self.xportMidi)
        #self.botonShowPartitura.clicked.connect(self.showPartitura)
        #self.botonStop.clicked.connect(self.stop)
        #self.botonStop.clicked.connect(self.converter_pdf_to_png())
    
    def Abrir_Modulo_Teoria(self):
        
            self.stackedWidget.setCurrentWidget(self.page_teoria)
            self.stackedWidget_2.setCurrentWidget(self.materia_profesor)
            materias = materiaFindAll()
            self.v_table = self.table_temas
            self.llenarDatosTable(materias)
            
            self.input_materias_search.setPlaceholderText("Buscar...")
            self.input_materias_search.textChanged.connect(self.searchTable)

            self.button_materias_ver_materia.clicked.connect(self.Abrir_Modulo_Sesiones)

    def Abrir_Modulo_Sesiones(self):
        if self.v_table.currentItem() != None:
            try:
                self.v_id_materia = int(self.v_table.currentItem().text())
            except:
                self.v_id_materia = -1
                self.mostrarAlerta("Error","Incorrecta celda seleccionada","Por favor seleccione solo el código")
        
        if self.v_id_materia != 0 and self.v_id_materia != -1:
            self.stackedWidget_2.setCurrentWidget(self.sesiones_profesor)
            sesiones = sesionFindAll(self.v_id_materia)
            self.v_table = self.table_sesiones
            self.llenarDatosTable(sesiones)
            
            self.input_sesiones_search.setPlaceholderText("Buscar...")
            self.input_sesiones_search.textChanged.connect(self.searchTable)

            self.button_sesiones_ver_sesion.clicked.connect(self.Abrir_Modulo_Actividades)
            self.button_sesiones_regresar.clicked.connect(self.Abrir_Modulo_Teoria)
        elif self.v_id_materia == -1:
            self.Abrir_Modulo_Teoria()
    
    def Abrir_Modulo_Actividades(self):
        if self.v_table.currentItem() != None:
            try:
                self.v_id_sesion = int(self.v_table.currentItem().text())
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

            self.button_actividades_ver_actividad.clicked.connect(self.Abrir_Modulo_Material_Actividad)
            self.button_actividades_regresar.clicked.connect(self.Abrir_Modulo_Sesiones)
        elif self.v_id_sesion == -1:
            self.Abrir_Modulo_Sesiones()

    def Abrir_Modulo_Material_Actividad(self):
        if self.v_table.currentItem() != None:
            try:
                self.v_id_actividad = int(self.v_table.currentItem().text())
            except:
                self.v_id_actividad = -1
                self.mostrarAlerta("Error","Incorrecta celda seleccionada","Por favor seleccione solo el código")
        
        if self.v_id_actividad != 0 and self.v_id_actividad != -1:
            self.stackedWidget_2.setCurrentWidget(self.material_actividad_profesor)
            material_actividades = actividadFindAll(self.v_id_actividad)
        elif self.v_id_actividad == -1:
            self.Abrir_Modulo_Actividades()
        button = "button_material"
        t = self.button_material_pro_crear.text()
        self.button_material_pro_crear.clicked.connect(functools.partial(self.button))
        

        self.button_material_actividad_regresar.clicked.connect(self.Abrir_Modulo_Actividades)
        self.llenarMaterial(material_actividades)

    def llenarMaterial(self, datos):
        
        scroll = self.scrollArea_3           # Scroll Area which contains the widgets, set as the centralWidget
        widget = QWidget()                 # Widget that contains the collection of Vertical Box
        vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        scroll.setGeometry(100,60,700,600)
        scroll.setWidgetResizable(True)

        #print(datos[0][5])
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
                    grid_2.addWidget(image, count_items, 0)
                    grid_2.addItem(space, count_items, 1)
                    count_items += 1
                    
                if tipo_material != "" and tipo_material[0][1] == "Audio":
                    btn_audio = QPushButton(str(datos_material[r][0]), self)
                    btn_audio.setObjectName(str(datos_material[r][0]))
                    btn_audio.clicked.connect(lambda: self.Reproducir_Audio_Material())
                    btn_audio.setStyleSheet("background-color: rgb(96, 189, 218); color: rgb(96, 189, 218); font-size: 1px;")
                    btn_audio.setIcon(QIcon('src/icons/icon_play.png'))
                    btn_audio.setIconSize(QSize(50, 50)) 
                    btn_audio.show()
                    grid_2.addWidget(btn_audio, count_items, 0)
                    grid_2.addItem(space, count_items, 1)
                    print("count_items audi", datos_material[r][0])
            
                vbox.addLayout(grid_2)

            grid = QGridLayout()
            grid.setHorizontalSpacing(6)

            #Horizontal spacer
            space = QSpacerItem(40, 20, QSizePolicy.Expanding)
            grid.addItem(space, 0, 0)

            #Boton agregar
            btn = QPushButton(str(datos[row_number][0]), self)
            btn.setObjectName(str(datos[row_number][0]))
            btn.clicked.connect(functools.partial(self.button))
            btn.setStyleSheet("background-color: rgb(96, 189, 218); color: rgb(96, 189, 218); font-size: 1px;")
            btn.setIcon(QIcon('src/icons/icon_home.png'))
            btn.setIconSize(QSize(50, 50)) 
            btn.show()
            grid.addWidget(btn, 0, 1)
            
            #Boton actualizar
            btn = QPushButton(str(datos[row_number][0]), self)
            btn.setObjectName(str(datos[row_number][0]))
            btn.clicked.connect(functools.partial(self.button))
            btn.setStyleSheet("background-color: rgb(86, 188, 75); color: rgb(86, 188, 75); font-size: 1px;")
            btn.setIcon(QIcon('src/icons/icon_home.png'))
            btn.setIconSize(QSize(50, 50)) 
            btn.show()
            grid.addWidget(btn, 0, 2)

            #boton eliminar
            btn = QPushButton(str(datos[row_number][0]), self)
            btn.setObjectName(str(datos[row_number][0]))
            btn.clicked.connect(functools.partial(self.button))
            btn.setStyleSheet("background-color: rgb(170, 0, 0); color: rgb(170, 0, 0); font-size: 1px;")
            btn.setIcon(QIcon('src/icons/icon_home.png'))
            btn.setIconSize(QSize(50, 50)) 
            btn.show()
            grid.addWidget(btn, 0, 3)
            grid.addItem(space, 0, 4)
            vbox.addLayout(grid)

        widget.setLayout(vbox)
        #Scroll Area Properties
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        self.show()

    def button(self):
        sender_button = self.sender().text()
        print(sender_button)

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
        for row_number, row_data in enumerate(datos):
            self.v_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.v_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    
    def mostrarAlerta(self, title, text, descripcion):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setInformativeText(descripcion)
        msg.exec_()

    
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
        print()                  
        shutil.copyfile(partitura_Pdf, "src/pdf/pdf_profesor/partitura.pdf")
        rta=converter_pdf_to_png()
        print(rta)



    def xportMidi(self):
        file_in = "src/audio/audio_voz_natural.wav"
        file_out = "src/export_midi/audio_piano_midi.mid"
        audio_data, srate = librosa.load(file_in, sr=None)
        midi = wave_to_midi(audio_data, srate=srate)
        with open (file_out, 'wb') as file:
            midi.writeFile(file)
        print("Done export file MIDI")

    def showPartitura(self):
        from asyncio import subprocess
        import subprocess
        #path = 'src\pdf\tareas.pdf'
        path = 'tareas.pdf'
        subprocess.Popen([path], shell=True)
        print("open partiture...")

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
                id_ruta=insertar_materialXactividad(3,file_path+file_save,'',2,self.v_id_usuario,1)
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
        
        #print(porcentaje)
    
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
