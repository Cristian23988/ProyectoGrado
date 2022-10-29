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

import publicador # publicador.py --> PublicaNota() --> numeroMIDI, frecHz, notaProxima, distNotaProxima

s = stream.Stream()

class Proceso(QObject):
    def __init__(self):
        super(Proceso, self).__init__()
        
    def procesoPub(self):
        publicador.PublicaNota()
        
class Ventana(QMainWindow):
    def __init__(self):
        super(Ventana, self).__init__()
        uic.loadUi("ui/diseno.ui", self)  #P1: mostraba la GUI  disenofinal.ui
        
        #self.botonMidi.clicked.connect(self.xportMidi)
        #self.botonShowPartitura.clicked.connect(self.showPartitura)
        #self.botonStop.clicked.connect(self.stop)
        #self.botonStop.clicked.connect(self.converter_pdf_to_png())
        

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

    def converter_pdf_to_png(self):
        
        import fitz
        file_path = "src/pdf/fire.pdf"
        
        zoom = 4  # zoom factor
        # PDF Page is converted into a whole picture 1056*816 and then for each picture a screenshot is taken.
        # zoom = 1.33333333 -----> Image size = 1056*816
        # zoom = 2 ---> 2 * Default Resolution (text is clear, image text is hard to read)    = filesize small / Image size = 1584*1224
        # zoom = 4 ---> 4 * Default Resolution (text is clear, image text is barely readable) = filesize large
        # zoom = 8 ---> 8 * Default Resolution (text is clear, image text is readable) = filesize large
        

        magnify = fitz.Matrix(zoom, zoom)  # magnifies in x, resp. y direction
        doc = fitz.open(file_path)  # open document
        i=1
        for page in doc:
            pix = page.get_pixmap(matrix=magnify)  # render page to an image
            pix.save(f"page-{page.number}.jpg")
            i=i+1
        #return "si"

    def actualizaVentana(self): #Recibe los datos: numeroMIDI, frecHz, notaProxima, distNotaProxima
       #el numero MIDI varia de 39 a 65 
        pub_numeroMIDI =  "%.2f" % (publicador.numeroMIDI) #tomamos solo 2 decimales
        self.ResMidi.setText(str(pub_numeroMIDI)) #actualizamos etiqueta MIDI
        
        pub_frecHz =  "%.2f" % (publicador.frecHz)
        self.ResFrec.setText(str(pub_frecHz)) #actualizamos etiqueta frec Hz
        
        self.ResNota.setText(str(publicador.notaProxima))  #actualizamos etiqueta Nota Prox                   
        #print("notasaaa:",publicador.notaProxima)
        if(publicador.frecHz > 95):
            n1 = note.Note(publicador.notaActual, quarterLength = 1) #publicador.elapsed_time)
            #print(publicador.notaActual)
            s.append([n1])
                            
        distNP = "%.2f" % (publicador.distNotaProxima)
        self.ResDist.setText(str(distNP)) #actualizamos etiqueta distancia a la nota prox
        
        self.verticalSlider.setValue(int((publicador.numeroMIDI)*10)) #actualizamos slider
        
def run():
    app = QApplication(sys.argv)
    programa = Ventana()
    programa.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    
    run()
