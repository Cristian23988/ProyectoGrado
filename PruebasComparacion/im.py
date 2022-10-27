import numpy as np 
import matplotlib.pyplot as plt 
from glob import glob
import librosa as lr
import librosa.display
audio1='DrumMaqueta'
y, sr = lr.load('./{}.wav'.format(audio1))
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
#plt.subplot(4, 2, 2)
#lr.display.specshow(D, y_axis='log')
#plt.colorbar(format='%+2.0f dB')
#plt.title('Log-frequency power spectrogram')
#plt.show()

audio2='input_file'
y, sr = lr.load('./{}.wav'.format(audio2))
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
plt.subplot(4, 2, 2)
lr.display.specshow(D, y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Log-frequency power spectrogram')
plt.show()