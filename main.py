#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 11:40:26 2019

@author: EDUCARTE
"""

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

import time
import publicador # publicador.py --> PublicaNota() --> numeroMIDI, frecHz, notaProxima, distNotaProxima

#MIDI
s = stream.Stream()

class Proceso(QObject):   # frec 7Hz
    def __init__(self):
        super(Proceso, self).__init__()
        
    def procesoPub(self):
        publicador.PublicaNota()
        
class Ventana(QMainWindow):  # 60Hz --> 100Hz
    def __init__(self):
        super(Ventana, self).__init__()
        uic.loadUi("disenofinal.ui", self)  #P1: mostraba la GUI  disenofinal.ui
        
        #Usamos multihilos Qt
        #self.hilo = QThread()
        #self.proceso = Proceso()
        #self.proceso.moveToThread(self.hilo)
        
        #self.boton.clicked.connect(self.hilo.start)
        self.botonMidi.clicked.connect(self.xportMidi)
        self.botonShowPartitura.clicked.connect(self.showPartitura)
        #self.hilo.started.connect(self.proceso.procesoPub)  #P2: Comienza el programa principal "publicador.py"
        #self.botonStop.clicked.connect(self.sstop)

        #self.timer = QTimer()
        #self.timer.setInterval(10) # cada 10ms se actualiza la ventana (100Hz)
        #self.timer.timeout.connect(self.actualizaVentana)
        #self.timer.start()

    def xportMidi(self):
        #n1 = note.Note(publicador.notaProxima, quarterLength = 1)
        #s.write('midi', fp='my_melody.mid')

        print("Starting...")
        file_in = "input_file.wav"
        file_out = "voiceMidi.mid"
        audio_data, srate = librosa.load(file_in, sr=None)
        print("Audio file loaded!")
        midi = wave_to_midi(audio_data, srate=srate)
        print("Conversion finished!")
        with open (file_out, 'wb') as file:
            midi.writeFile(file)
        print("Done. Exiting!")

    def showPartitura(self):
        from asyncio import subprocess
        import subprocess
        path='tareas.pdf'
        subprocess.Popen([path], shell=True)
        

    def sstop(self):
        #self.timer.stop()
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
        
        
#P1: mostraba la GUI  disenofinal.ui
def run():
    app = QApplication(sys.argv)
    programa = Ventana()
    programa.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    run()
