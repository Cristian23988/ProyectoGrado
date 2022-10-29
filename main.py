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
        uic.loadUi("ui/disenofinal.ui", self)  #P1: mostraba la GUI  disenofinal.ui
        
        self.botonMidi.clicked.connect(self.xportMidi)
        self.botonShowPartitura.clicked.connect(self.showPartitura)
        self.botonStop.clicked.connect(self.stop)

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
