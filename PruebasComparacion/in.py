import numpy as np
import matplotlib.pyplot as plt
import mido as md

# INGRESO
archivomid = 'voiceMidi.mid'
archivomidestudiante='output_file.mid'
# instrumento
canal = 'channel=0' 
# para pmf
tramos = 20     

# PROCEDIMIENTO
# Abre archivo midi
def mostrar_parti(midi):
    partitura = md.MidiFile(midi)

    # un instrumento, tabla de notas
    accion = 'note_on'
    tabla = []
    for dato in partitura:
        linea = str(dato)
        parte = linea.split(' ')
        if (parte[0]==accion and parte[1]==canal):
            valor = parte[2].split('=')
            nota = int(valor[1])
            valor = parte[3].split('=')
            velocidad = int(valor[1])
            valor = parte[4].split('=')
            tiempo = float(valor[1])
            tabla.append([nota, velocidad, tiempo])
    # NOTAS, Velocity y tempo() 
    print("Notas del MIDI: ",tabla)
    data=tabla
    tabla = np.array(tabla)

    #Cantidad de notas que detecta en cada MIDI (m)
    m = len(tabla)
    

    # Cuenta de tiempos
    xmin = 0
    xmax = np.round((np.max(tabla[:,2])*1.1),2)
    muestreo = tramos +1
    x = np.linspace(xmin,xmax,muestreo)
    deltax = x[1]-x[0]
    cuenta = np.zeros(muestreo,dtype=int)
    for f in range(0,m,1):
        valor = tabla[f,2]
        encuentra = 0
        j=0
        while not(j>=muestreo or encuentra==1):
            if x[j]>valor:
                cuenta[j-1] = cuenta[j-1]+1
                encuentra=1
            j=j+1
    frelativa = cuenta/np.sum(cuenta)
    acumulada = np.cumsum(frelativa)
                
    # SALIDA
    # Presenta pistas
    pistas = partitura.tracks
    n = len(pistas)
    print('pistas/instrumentos: ')
    #for i in range(0,n,1):
        #print(i, pistas[i])
    #    print()
    # Tabulados
    # print('Tabulados: ')
    # print('     x: ',x)
    # print('cuenta: ', cuenta)
    return data

archivo1=mostrar_parti(archivomid)
archivo2=mostrar_parti(archivomidestudiante)
#print("Common Elements", set(archivo1) & set(archivo2))
print("Comparar notas: ")
for i in archivo1[:]:
    for j in archivo2[:]:
        print(i[:1]," - ",j[:1])
        if(i[:1]==j[:1]):
            print("if",i)
        
            break
    

# GRAFICAS
# plt.subplot(211)
# plt.bar(x,frelativa, width=deltax*0.8, align='edge')
# plt.title(archivomid + ' , ' + canal)
# #plt.ylabel('pmf')

# plt.subplot(212)
# plt.plot(x,acumulada,'m')
# plt.ylabel('cdf')
# #plt.show()