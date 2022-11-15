from ctypes import pointer
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic # llama al archivo disenofinal.ui
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
from partitureConversion.MIDIUtil.src.midiutil.MidiFile3 import MIDIFile
from Comparacion.compare import comparacion_wav
from conexion.evidencia_estudiante import insert as insertar_evidencia
from conexion.notas import insert as insertarNota
from conexion.material_actividad import insert as insertar_materialXactividad

s = stream.Stream()
        
class Ventana(QMainWindow):
    
    def __init__(self):
        super(Ventana, self).__init__()
        uic.loadUi("ui/diseno.ui", self)  #P1: mostraba la GUI  disenofinal.ui
        
        self.button_menu_home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_home))
        self.button_menu_teoria.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_teoria))
        self.button_menu_practicas.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_practicas))
        self.button_menu_quiz.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_quiz))
        self.button_menu_profesor.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_profesor))

        self.button_home_teoria.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_teoria))
        self.button_home_practicas.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_practicas))
        self.button_home_quiz.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_quiz))
        #Grabar y reproducir audio-----------------------
        self.button_practicas_record.clicked.connect(self.grabar_estudiante)
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
        print("teoria")        
    def Abrir_Modulo_Practica(self):
        print("practica")                    
    def Abrir_Modulo_Quiz(self):
        print("quiz") 
    def prueba_compare(self):
        comparacion_practica(self)
    def grabar_estudiante(self):
        rol='estudiante'
        self.id_ruta=Grabar_Audio(rol)
    def grabar_profesor(self):
        rol='profesor'
        self.id_rutaGrabar_Audio(rol)

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

def Grabar_Audio(rol):
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
        if (rol == 'estudiante'):
            file_save='voz_solfeo.wav' 
            file_path='src/audio/audio_de_estudiante/'
            id_ruta=insertar_evidencia(file_path+file_save,10)
        elif (rol == 'profesor'):
            file_save='audio_profesor.wav' 
            file_path='src/audio/audio_de_profesor/'
            id_ruta=insertar_materialXactividad(3,file_path+file_save,'',2,2,1)
        wv.write(file_path+file_save, recording, frequency, sampwidth=2)
        Convertir_Audio_A_MIDI(file_path+file_save,rol)
        
        print('Finalizado con exito')  
        return id_ruta     

def Convertir_Audio_A_MIDI(file_in,rol):
        import librosa
        from sound_to_midi.monophonic import wave_to_midi
        print("Starting...")
        #file_in = "Basepiano.wav"
        file_out = ""
        if (rol == 'estudiante'):
            file_out = "src/export_midi/estudiante/audio_estudiante.mid"
        elif (rol == 'profesor'):
            file_out = "src/export_midi/profesor/midi_partiture.mid"
        
        audio_data, srate = librosa.load(file_in, sr=None)
        print("Audio file loaded!")
        midi = wave_to_midi(audio_data, srate=srate)
        print("Conversion finished!")
        with open (file_out, 'wb') as file:
            midi.writeFile(file)
        print("Done. Exiting!")

        
        if (rol == 'estudiante'):
            Midi_to_piano_Estudiante(file_out)
        elif (rol == 'profesor'):
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
        insertarNota(13,5,porcentaje,1,self.id_ruta)
        
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
    rol='profesor'
    rta=midi_to_wav.Ejemplo.run(ruta_midi_to_piano,file_output,rol) 
    print(rta)

def Midi_to_piano_Estudiante(ruta_midi_to_piano):
    import  midi_to_wav
    from mido import MidiFile
    #ruta_midi_to_piano='src/export_midi/estudiante/audio_piano_midi.mid'
    rol='estudiante'
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
