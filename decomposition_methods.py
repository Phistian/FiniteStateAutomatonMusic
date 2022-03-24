from music21 import *


def linearize(list_of_songs):
    big_stream = stream.Stream()
    for song in list_of_songs:
        parts = song.getElementsByClass('Part')
        for par in parts:
            measures = par.getElementsByClass('Measure')
            for meas in measures:
                ns = meas.getElementsByClass('Note')
                for n in ns:
                    big_stream.append(n)

    return big_stream


def change_key(song, desired_pitch):
    k = song.analyze('key')
    i = interval.Interval(k.tonic, pitch.Pitch(desired_pitch))
    return song.transpose(i)


def count_notes_and_duration(part, dict_frequencies = {}):

    for item in part:

        dur = item.duration
        s_dur = ', ' + str(dur.quarterLength) + ']'
        s_pitch = '[' + item.nameWithOctave
        if item.nameWithOctave in dict_frequencies:
            dict_frequencies[s_pitch + s_dur] = dict_frequencies[s_pitch + s_dur] + 1
        else:
            dict_frequencies[s_pitch + s_dur] = 1

    total = sum(dict_frequencies.values())
    for key in dict_frequencies:
        dict_frequencies[key] = dict_frequencies[key]/total

    return dict_frequencies


def count_pitches(part, dict_frequencies = {}):

    for item in part:

        s_pitch = item.nameWithOctave
        if s_pitch in dict_frequencies:
            dict_frequencies[s_pitch] = dict_frequencies[s_pitch] + 1
        else:
            dict_frequencies[s_pitch] = 1

    total = sum(dict_frequencies.values())
    for key in dict_frequencies:
        dict_frequencies[key] = dict_frequencies[key]/total
    return dict_frequencies, list(dict_frequencies.values()), list(dict_frequencies.keys())


def count_durations(part, dict_frequencies = {}):

    for item in part:

        dur = item.duration
        s_dur = dur.quarterLength
        if s_dur in dict_frequencies:
            dict_frequencies[s_dur] = dict_frequencies[s_dur] + 1
        else:
            dict_frequencies[s_dur] = 1

    total = sum(dict_frequencies.values())
    for key in dict_frequencies:
        dict_frequencies[key] = dict_frequencies[key]/total

    return dict_frequencies, list(dict_frequencies.values()), list(dict_frequencies.keys())


def count_pitch_pairs(part, pair_frequencies=[], encountered_states=[]):
    for i in range(1,len(part)):
        state = part[i-1].nameWithOctave
        new_state = part[i].nameWithOctave
        state_pairing = [state,new_state]
        if state_pairing in encountered_states:
            index = encountered_states.index(state_pairing)
            pair_frequencies[index] = pair_frequencies[index] + 1
        else:
            encountered_states.append(state_pairing)
            pair_frequencies.append(1)

    total = sum(pair_frequencies)
    for i in range(0,len(pair_frequencies)):
        pair_frequencies[i] = pair_frequencies[i]/total

    return pair_frequencies, encountered_states


def count_pitch_sequences(input, k, frequencies=[], encountered=[]):
    window_size = k-1
    ws = window_size
    for t in range(0, len(input)-ws):

        #  What is the state?
        state = []
        for i in range(0, ws):
            state.append(input[t+i].nameWithOctave)
        successor = input[t+ws].nameWithOctave
        encounter = [state, successor]

        #  Has this been seen before?
        if encounter in encountered:
            index = encountered.index(encounter)
            frequencies[index] += 1
        else:
            encountered.append(encounter)
            frequencies.append(1)

    #  Normalize frequencies to probability distribution
    norm = sum(frequencies)
    for i in range(0, len(frequencies)):
        frequencies[i] /= norm

    return frequencies, encountered


def count_duration_sequences(input, k, frequencies=[], encountered=[]):
    window_size = k-1
    ws = window_size
    for t in range(0, len(input)-ws):

        #  What is the state?
        state = []
        for i in range(0, ws):
            state.append(input[t+i].duration.quarterLength)
        successor = input[t+ws].duration.quarterLength
        encounter = [state, successor]

        #  Has this been seen before?
        if encounter in encountered:
            index = encountered.index(encounter)
            frequencies[index] += 1
        else:
            encountered.append(encounter)
            frequencies.append(1)

    #  Normalize frequencies to probability distribution
    norm = sum(frequencies)
    for i in range(0, len(frequencies)):
        frequencies[i] /= norm

    return frequencies, encountered


