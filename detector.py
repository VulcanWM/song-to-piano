import numpy as np
from audio_processing import detect_peaks

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def detect_chord_normal(audio, sample_rate, threshold_float):
    peaks = detect_peaks(audio, sample_rate, threshold_float)

    # convert frequency to note
    midi_notes = []

    for frequency, _ in peaks:
        midi = round(69 + 12 * np.log2(frequency / 440))
        midi_notes.append(midi)

    midi_notes = sorted(set(midi_notes))

    # detect chord
    pitch_classes = {midi % 12 for midi in midi_notes}

    for root in range(12):
        major = {(root + interval) % 12 for interval in [0, 4, 7]}
        minor = {(root + interval) % 12 for interval in [0, 3, 7]}

        if major.issubset(pitch_classes):
            return NOTE_NAMES[root] + " Major"

        if minor.issubset(pitch_classes):
            return NOTE_NAMES[root] + " Minor"

    return None

def detect_chord_weighted(audio, sample_rate, threshold_float):
    peaks = detect_peaks(audio, sample_rate, threshold_float)

    pitch_strengths = np.zeros(12)

    for frequency, magnitude in peaks:
        midi = round(69 + 12 * np.log2(frequency / 440))
        pitch_class = midi % 12

        pitch_strengths[pitch_class] += magnitude

    # detect chord

    chord_strengths = []
    for root in range(12):
        major = {(root + interval) % 12 for interval in [0, 4, 7]}
        minor = {(root + interval) % 12 for interval in [0, 3, 7]}

        chord_strengths.append(sum(pitch_strengths[i] for i in major))
        chord_strengths.append(sum(pitch_strengths[i] for i in minor))

    if not np.any(pitch_strengths):
        return None

    chord_index = np.argmax(chord_strengths)

    tonic = NOTE_NAMES[chord_index // 2]
    tonality = " Major" if chord_index % 2 == 0 else " Minor"

    return tonic + tonality