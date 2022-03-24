import numpy as np
from decomposition_methods import *
from markov_chain import *

#TODO: Unfinished
def compute_density_entropy(big_stream):
    p_f = count_pitch_sequences(big_stream, 1)[0]
    dur_f = count_duration_sequences(big_stream, 1)[0]


def compute_block_entropy(big_stream, m, normalized=False):
    if m == 0:
        return 0, 0
    elif m == 1:
        p_frequencies = count_pitches(big_stream)[1]
        dur_frequencies = count_durations(big_stream)[1]
        p_np_freq = np.array(p_frequencies)
        dur_np_freq = np.array(dur_frequencies)
        p_alphabet_length = compute_alphabet_length(type='piano')
        dur_alphabet_length = compute_alphabet_length(type='normal durations')
    else:  # This calculation is different, because when m > 1, windows sweep over the stream. Another type of output.
        p_frequencies, p_e = count_pitch_sequences(big_stream, m, [], [])
        dur_frequencies, dur_e = count_duration_sequences(big_stream, m, [], [])
        p_np_freq = np.array(p_frequencies)
        dur_np_freq = np.array(dur_frequencies)
        p_alphabet_length = compute_alphabet_length(type='piano')
        dur_alphabet_length = compute_alphabet_length(type='normal durations')
        #print(dur_alphabet_length)
        #print(dur_e)

    if normalized:
        p_block_entropy = sum(p_np_freq * np.log(1/p_np_freq) / np.log(p_alphabet_length))
        dur_block_entropy = sum(dur_np_freq * np.log(1 / dur_np_freq) / np.log(dur_alphabet_length))
        print('here')
    else:

        p_block_entropy = sum(p_np_freq * np.log2(1 / p_np_freq))
        dur_block_entropy = sum(dur_np_freq * np.log2(1 / dur_np_freq))
        if sum(p_np_freq) == p_np_freq[0]*len(p_np_freq):
            p_block_entropy = np.log2(len(p_np_freq))
        if sum(dur_np_freq) == dur_np_freq[0]*len(dur_np_freq):
            dur_block_entropy = np.log2(len(dur_np_freq))

    return p_block_entropy, dur_block_entropy


def compute_k1(big_stream):
    p_density_entropy, dur_density_entropy = compute_block_entropy(big_stream,1)
    p_e = count_pitches(big_stream, {})[2]
    dur_e = count_durations(big_stream, {})[2]
    p_alphabet_length = compute_alphabet_length(p_e, type='piano')
    dur_alphabet_length = compute_alphabet_length(dur_e, type='normal durations')
    p_k1 = np.log2(p_alphabet_length) - p_density_entropy
    dur_k1 = np.log2(dur_alphabet_length) - dur_density_entropy
    return p_k1, dur_k1


def compute_alphabet_length(encountered=[], type='none'):
    if type == 'piano':
        return 88  # 88-key piano
    elif type == 'normal durations':
        return 4*8 + 3  # 8 quarter-steps (1->8) plus 4 possible sixteenth-steps (0,0.25,0.50,0.75) plus 0.x.
    pitch_collection = []

    if isinstance(encountered[0], list):  # Means m > 1. We have used a window to sweep over stream & get statistics.
        for stateory in encountered:
            history_states = stateory[0]
            resulting_state = stateory[1]
            for history_state in history_states:
                if history_state not in pitch_collection:
                    pitch_collection.append(history_state)
            if resulting_state not in pitch_collection:
                pitch_collection.append(stateory[1])

    else:  # This means we're using a list from density probability calculations.
        for state in encountered:
            if state not in pitch_collection:
                pitch_collection.append(state)
    alphabet_length = len(pitch_collection)
    return alphabet_length


def compute_hm(big_stream, m):
    if m < 1:
        raise Exception('A small m was inputted into hm-calculation.')
    s_m = np.array(compute_block_entropy(big_stream, m))
    s_m_minus1 = np.array(compute_block_entropy(big_stream, m-1))
    delta_block_entropy = s_m - s_m_minus1
    return delta_block_entropy[0], delta_block_entropy[1]


def compute_entropy_delta_S(max_non_zero_k, alphabet_length, frequencies_collection):  #
    block_entropy1 = frequencies_collection[max_non_zero_k - 1]
    block_entropy2 = frequencies_collection[max_non_zero_k]
    delta_S = block_entropy2 - block_entropy1


def compute_km(big_stream, m):
    if m < 2:
        raise Exception('A small m was inputted into km-calculation.')
    s_m = np.array(compute_block_entropy(big_stream, m))
    s_m_minus1 = np.array(compute_block_entropy(big_stream, m - 1))
    s_m_minus2 = np.array(compute_block_entropy(big_stream, m - 2))
    km_p_dur = -s_m + 2 * s_m_minus1 - s_m_minus2
    return km_p_dur[0], km_p_dur[1]


def compute_kcorr(big_stream):  # Assumption is made here that this function is used on self created music.
    #p_e = count_pitch_sequences(big_stream, 1)[1]
    #dur_e = count_duration_sequences(big_stream, 1)[1]
    p_alph_length = compute_alphabet_length(type='piano')
    dur_alph_length = compute_alphabet_length(type='normal durations')

    p_k_list = []
    k1 = compute_k1(big_stream)[0]  # Otherwise, one km being zero does not imply the next being zero.
    k = k1
    m = 1
    while k > np.log2(p_alph_length)/500:
        p_k_list.append(k)
        m += 1
        k = compute_km(big_stream, m)[0]

    else:
        print('Stopping p_kcorr calculation before km, m = ' + str(m) + '. km = ' + str(k) + '.')
    p_kcorr = sum(p_k_list)

    dur_k_list = []
    k1 = compute_k1(big_stream)[1]  # Otherwise, one km being zero does not imply the next being zero.
    k = k1
    m = 1
    while k > np.log2(dur_alph_length)/500:
        dur_k_list.append(k)
        m += 1
        k = compute_km(big_stream, m)[1]
    else:
        print('Stopping dur_kcorr calculation before km, m = ' + str(m) + '. km = ' + str(k) + '.')
    dur_kcorr = sum(dur_k_list)

    return p_kcorr, dur_kcorr, p_k_list, dur_k_list
