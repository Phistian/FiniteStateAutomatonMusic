from music21 import *
import random

def create_stream_from_density(length, instruments, p_freq, p_enc, dur_freq, dur_enc):

    created_score = stream.Score()

    part = stream.Part()
    created_score.append(part)



    for i in range(0, length-1):

        pitch_choice = random.choices(p_enc, p_freq)[0]
        duration_choice = random.choices(dur_enc, dur_freq)[0]
        note_addition = note.Note(pitch_choice)
        note_addition.quarterLength = duration_choice
        part.append(note_addition)

    return created_score


def create_stream_from_k2_correlations(length, instruments, pitches_frequencies, encountered_phrases, duration_density):

    created_score = stream.Score()

    duration_weights = list(duration_density.values())
    durations = list(duration_density.keys())
    indices = range(0,len(encountered_phrases))

    part = stream.Part()
    created_score.append(part)

    first_i = random.choices(indices, pitches_frequencies)[0]
    for i in range(0,1):
        early_note_name = encountered_phrases[first_i][i]  # Picks out a pair of notes.
        early_note = note.Note(early_note_name)
        early_duration = random.choices(durations, duration_weights)[0]
        early_note.quarterLength = early_duration
        part.append(early_note)



    for i in range(0, length-1):
        temp_possibilities = []
        temp_probabilities = []
        current_state = part[-1].nameWithOctave
        #print(current_state)
        for j in range(0, len(encountered_phrases)):
            phrase = encountered_phrases[j]
            phrase_state = phrase[0]
            phrase_successor = phrase[1]
            if current_state == phrase_state:
                temp_possibilities.append(phrase_successor)
                temp_probabilities.append(pitches_frequencies[j])
        for k in range(0, len(temp_probabilities)):
            temp_probabilities[k] = temp_probabilities[k]/sum(temp_probabilities)  # Normalizing

        pitch_choice = random.choices(temp_possibilities, temp_probabilities)[0]
        duration_choice = random.choices(durations, duration_weights)[0]
        note_addition = note.Note(pitch_choice)
        note_addition.quarterLength = duration_choice
        part.append(note_addition)

    return created_score


def create_stream_k(stream_len, k, p_freq, p_enc, dur_dens):
    created_score = stream.Score()
    treble = clef.TrebleClef()
    created_score.append(treble)

    duration_weights = list(dur_dens.values())
    durations = list(dur_dens.keys())
    indices = range(0,len(p_enc))

    part = stream.Part()
    created_score.append(part)

    first_i = random.choices(indices, p_freq)[0]
    for i in range(0, k-1):
        early_note_name = p_enc[first_i][0][i]  # Picks out a k-sequence of notes.

        early_note = note.Note(early_note_name)
        early_duration = random.choices(durations, duration_weights)[0]
        early_note.quarterLength = early_duration
        part.append(early_note)


    for i in range(0, stream_len - 1):
        temp_possibilities = []
        temp_probabilities = []
        current_state = []

        print(k)
        for j in range(-k+1, 0):
            #print(j)
            current_state.append(part[j].nameWithOctave)


        for j in range(0, len(p_enc)):
            phrase = p_enc[j]
            phrase_state = phrase[0]
            phrase_successor = phrase[1]
            if current_state == phrase_state:
                temp_possibilities.append(phrase_successor)
                temp_probabilities.append(p_freq[j])

        if temp_probabilities == []:
            print('Reached a state with no successor. Stopping.')
            return created_score




        for j in range(0, len(temp_probabilities)):
            temp_probabilities[j] = temp_probabilities[j]/sum(temp_probabilities)  # Normalizing

        pitch_choice = random.choices(temp_possibilities, temp_probabilities)[0]
        duration_choice = random.choices(durations, duration_weights)[0]
        note_addition = note.Note(pitch_choice)
        note_addition.quarterLength = duration_choice
        part.append(note_addition)

    return created_score


def create_stream_kk(stream_len, p_k, dur_k, p_freq, p_enc, dur_freq, dur_enc):
    if p_k == 1 and dur_k == 1:
        piece = create_stream_from_density(stream_len, [], p_freq, p_enc, dur_freq, dur_enc)
        return piece

    created_score = stream.Score()
    treble = clef.TrebleClef()
    created_score.append(treble)
    dur_list = []

    p_indices = range(0,len(p_enc))
    dur_indices = range(0, len(dur_enc))

    part = stream.Part()
    created_score.append(part)


    first_p_i = random.choices(p_indices, p_freq)[0]
    first_dur_i = random.choices(dur_indices, dur_freq)[0]
    for i in range(0, dur_k-1):
        early_dur = dur_enc[first_dur_i][0][i]  # Picks out a k-sequence of notes.
        dur_list.append(early_dur)
    for i in range(0, p_k-1):
        early_note_name = p_enc[first_p_i][0][i]  # Picks out a k-sequence of notes.
        early_note = note.Note(early_note_name)
        early_note.quarterLength = dur_list[i]
        part.append(early_note)



    for i in range(0, stream_len - 1):
        temp_possibilities = []
        temp_probabilities = []
        current_state = []

        for j in range(-dur_k + 1, 0):
            # print(j)
            current_state.append(dur_list[j])

        for j in range(0, len(dur_enc)):
            phrase = dur_enc[j]
            phrase_state = phrase[0]
            phrase_successor = phrase[1]
            if current_state == phrase_state:
                temp_possibilities.append(phrase_successor)
                temp_probabilities.append(dur_freq[j])

        if temp_probabilities == []:
            print('Reached a duration state with no successor. Stopping.')
            return created_score

        for j in range(0, len(temp_probabilities)):
            temp_probabilities[j] = temp_probabilities[j] / sum(temp_probabilities)  # Normalizing

        dur_choice = random.choices(temp_possibilities, temp_probabilities)[0]
        dur_list.append(dur_choice)

    for i in range(0, stream_len - 1):
        temp_possibilities = []
        temp_probabilities = []
        current_state = []

        for j in range(-p_k+1, 0):
            #print(j)
            current_state.append(part[j].nameWithOctave)


        for j in range(0, len(p_enc)):
            phrase = p_enc[j]
            phrase_state = phrase[0]
            phrase_successor = phrase[1]
            if current_state == phrase_state:
                temp_possibilities.append(phrase_successor)
                temp_probabilities.append(p_freq[j])

        if temp_probabilities == []:
            print('Reached a state with no successor. Stopping.')
            return created_score


        for j in range(0, len(temp_probabilities)):
            temp_probabilities[j] = temp_probabilities[j]/sum(temp_probabilities)  # Normalizing

        pitch_choice = random.choices(temp_possibilities, temp_probabilities)[0]
        note_addition = note.Note(pitch_choice)
        note_addition.quarterLength = dur_list[p_k-2 + i]  # We have already used p_k-1 dur_list values in early notes.
        part.append(note_addition)

    return created_score


