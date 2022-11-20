import librosa
import librosa.display
import matplotlib.pyplot as plt
from dtw import dtw
from numpy.linalg import norm

def comparacion_wav(audio_prof,audio_est):
        #Loading audio files
        Path_estudiante='src/audio/compare/estudiante/output_estudiante.wav'
        Path_profesor='src/audio/compare/profesor/output_profesor.wav'
        y1, sr1 = librosa.load(Path_estudiante) 

        y2, sr2 = librosa.load(Path_profesor) 

        # y1, sr1 = librosa.load('src/audio/audio_piano.wav') 

        # y2, sr2 = librosa.load('src/audio/audio_voz_natural.wav') 

        #Showing multiple plots using subplot
        plt.subplot(1, 3, 1,facecolor='red') 
        mfcc1 = librosa.feature.mfcc(y1,sr1)   #Computing MFCC values
        print("mfcc:   ",mfcc1)
        librosa.display.specshow(mfcc1)

        plt.subplot(1, 3, 2,facecolor='red')
        mfcc2 = librosa.feature.mfcc(y2, sr2)
        print("mfcc:   ",mfcc2)
        librosa.display.specshow(mfcc2)

        dist, cost, acc_cost, path = dtw(mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=1))
        print("The normalized distance between the two : ",dist)   # 0 for similar audios 
        # print("cost : ",cost)
        # print("acc_cost : ",acc_cost)
        # print("path : ",path)
        plt.subplot(1, 3, 3)
        #plt.subplot()
        plt.imshow(cost.T, origin='lower', cmap=plt.get_cmap('gray'), interpolation='nearest')
        plt.plot(path[0], path[1], 'w')   #creating plot for DTW

        plt.show()  #To display the plots graphically
        return dist
#comparacion_wav('audio_profesor.wav','voz_solfeo.wav')