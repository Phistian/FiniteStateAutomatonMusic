from music21 import *
from decomposition_methods import *
from markov_chain import *
from measures import *
import numpy
from matplotlib import pyplot as plt

bach_list = []
song_list = ['bach/bwv297.mxl']#, 'bach/bwv362.mxl', 'bach/bwv355.mxl', 'bach/bwv340.mxl', 'bach/bwv111.6.mxl']

for song in song_list:
    m21_song = corpus.parse(song)
    change_key(m21_song, 'C')
    bach_list.append(m21_song)
big_stream = linearize(bach_list)





k = 2
p_k = k
dur_k = k

if p_k == 1:
    pitch_frequencies, pitch_encounters = count_pitches(big_stream, {})[1:3]
else:
    pitch_frequencies, pitch_encounters = count_pitch_sequences(big_stream, k)
if dur_k == 1:
    duration_frequencies, duration_encounters = count_durations(big_stream, {})[1:3]
else:
    duration_frequencies, duration_encounters = count_duration_sequences(big_stream, dur_k)
print(pitch_encounters)

s = create_stream_kk(stream_len=1000, p_k=p_k, dur_k=dur_k, p_freq=pitch_frequencies, p_enc=pitch_encounters, dur_freq=duration_frequencies, dur_enc=duration_encounters)
print('made')
s.show()





## Plots (the first one was not included in the report) ##

## Block entropy plot
sm_v = []
m_v = np.array(range(1,1,4))
p_slope = []
dur_slope = []
for m in m_v:
    print(m)
    m = int(m)
    sm = np.array(compute_block_entropy(s[0], m))
    sm_v.append(sm)
plt.plot(m_v, sm_v)
plt.legend(['Pitch', 'Duration'])
plt.show()


## Correlation information plot
p_k_corr, dur_k_corr, p_k_list, dur_k_list = compute_kcorr(s[0])
print(p_k_corr - np.log2(88))
print(dur_k_corr - np.log2(4*8 + 3))
plt.bar(range(1,len(p_k_list)+1), p_k_list)
plt.title('Correlation Information, Pitch Sequence')
plt.xlabel('m')
plt.ylabel(u'k\u2098')
plt.show()
plt.bar(range(1,len(dur_k_list)+1), dur_k_list)
plt.title('Correlation Information, Duration Sequence')
plt.xlabel('m')
plt.ylabel(u'k\u2098')
plt.show()

entropy = compute_block_entropy(s[0], 1)
print(entropy)

