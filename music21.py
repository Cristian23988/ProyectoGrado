#from music21 import note, stream
#n = note.Note('D', quarterLength=1/4)
#n.show()
from music21 import note, stream

n1 = note.Note('E', quarterLength = 1)
n2 = note.Note('E', quarterLength = 1)
n3 = note.Note('B', quarterLength = 1)
n4 = note.Note('B', quarterLength = 1)
n5 = note.Note('C#5', quarterLength = 1)
n6 = note.Note('C#5', quarterLength = 1)
n7 = note.Note('B', quarterLength = 2)
n8 = note.Note('A', quarterLength = 1)
n9 = note.Note('A', quarterLength = 1)
n10 = note.Note('G#', quarterLength = 1)
n11 = note.Note('G#', quarterLength = 1)
n12 = note.Note('F#', quarterLength = 1)
n13 = note.Note('F#', quarterLength = 1)
n14 = note.Note('E', quarterLength = 2)

s = stream.Stream()
s.append([n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14])
#s.show() #Abre el programa musescore

s.write('midi', fp='my_melody.mid')
#s.write('musicxml.pdf', fp='my_melody_IA.pdf')