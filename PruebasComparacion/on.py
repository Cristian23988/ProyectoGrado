#Comparing them may be easier than I thought
from scipy.io.wavfile import read as wavread
import wave
w_one = wave.open('input_file.wav', 'r')
w_two = wave.open('input_file_copy.wav', 'r')
[samplerate, y] = wavread('input_file.wav')
[samplerate, z] = wavread('input_file_PruebaPiano.wav')
for x in range(0,samplerate,4): #Slight compression for the program to run faster.
    y1,y2 = [y[x][0], y[x][1]] #y1,y2 are numbers for your in Comparison.wav. Use these to compare to file 2.
    z1,z2 = [z[x][0], z[x][1]] #z1,z2 are numbers for you to compare.
    print(y1,y2," ",z1,z2)

if w_one.readframes() == w_two.readframes():
    print('exactly the same')
else:
    print('not a match')