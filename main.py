import soundfile as sf
import numpy as np

def detect_chord_normal(file, threshold_float):
    audio, sample_rate = sf.read(file)

    # convert stereo to mono if necessary
    if audio.ndim == 2:
        audio = np.mean(audio, axis=1)

    # calculate fourier transform
    fft = np.fft.rfft(audio)

    # calculate magnitude of each frequency
    magnitudes = np.abs(fft)

    # calculate which frequency each fft value represents
    frequencies = np.fft.rfftfreq(len(audio), d=1 / sample_rate)

    # detect the frequencies
    peaks = []
    threshold = threshold_float * np.max(magnitudes)

    for i in range(1, len(magnitudes) - 1):
        if (
                magnitudes[i] > magnitudes[i - 1]
                and magnitudes[i] > magnitudes[i + 1]
                and magnitudes[i] > threshold
        ):
            peaks.append(frequencies[i])

    # convert frequency to note
    midi_notes = []

    for frequency in peaks:
        midi = round(69 + 12 * np.log2(frequency / 440))
        midi_notes.append(midi)

    midi_notes = sorted(set(midi_notes))

    # detect chord
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    pitch_classes = {midi % 12 for midi in midi_notes}
    # print("detected pitch classes:", pitch_classes)

    for root in range(12):
        major = {(root + interval) % 12 for interval in [0, 4, 7]}
        minor = {(root + interval) % 12 for interval in [0, 3, 7]}

        if major.issubset(pitch_classes):
            return note_names[root] + " Major"

        if minor.issubset(pitch_classes):
            return note_names[root] + " Minor"

    return None

def detect_chord_weighted(file, threshold_float):
    audio, sample_rate = sf.read(file)

    # convert stereo to mono if necessary
    if audio.ndim == 2:
        audio = np.mean(audio, axis=1)

    # calculate fourier transform
    fft = np.fft.rfft(audio)

    # calculate magnitude of each frequency
    magnitudes = np.abs(fft)

    # calculate which frequency each fft value represents
    frequencies = np.fft.rfftfreq(len(audio), d=1 / sample_rate)

    # detect the frequencies
    peaks = []
    threshold = threshold_float * np.max(magnitudes)

    for i in range(1, len(magnitudes) - 1):
        if (
                magnitudes[i] > magnitudes[i - 1]
                and magnitudes[i] > magnitudes[i + 1]
                and magnitudes[i] > threshold
        ):
            peaks.append((frequencies[i], magnitudes[i]))

    pitch_strengths = np.zeros(12)

    for frequency, magnitude in peaks:
        midi = round(69 + 12 * np.log2(frequency / 440))
        pitch_class = midi % 12

        pitch_strengths[pitch_class] += magnitude

    # detect chord
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    chord_strengths = []
    for root in range(12):
        major = {(root + interval) % 12 for interval in [0, 4, 7]}
        minor = {(root + interval) % 12 for interval in [0, 3, 7]}

        chord_strengths.append(sum(pitch_strengths[i] for i in major))
        chord_strengths.append(sum(pitch_strengths[i] for i in minor))

    chord_index = np.argmax(chord_strengths)

    tonic = note_names[chord_index // 2]
    tonality = " Major" if chord_index % 2 == 0 else " Minor"

    return tonic + tonality

threshold_float = 0.2

print("Threshold:", threshold_float)

files = [
"all_chords/c-major.wav",
  "all_chords/c-minor.wav",
  "all_chords/c-sharp-major.wav",
  "all_chords/c-sharp-minor.wav",
  "all_chords/d-major.wav",
  "all_chords/d-minor.wav",
  "all_chords/d-sharp-major.wav",
  "all_chords/d-sharp-minor.wav",
  "all_chords/e-major.wav",
  "all_chords/e-minor.wav",
  "all_chords/f-major.wav",
  "all_chords/f-minor.wav",
  "all_chords/f-sharp-major.wav",
  "all_chords/f-sharp-minor.wav",
  "all_chords/g-major.wav",
  "all_chords/g-minor.wav",
  "all_chords/g-sharp-major.wav",
  "all_chords/g-sharp-minor.wav",
  "all_chords/a-major.wav",
  "all_chords/a-minor.wav",
  "all_chords/a-sharp-major.wav",
  "all_chords/a-sharp-minor.wav",
  "all_chords/b-major.wav",
  "all_chords/b-minor.wav"
]


both_correctly_identified = set()
normal_only_correctly_identified = set()
weighted_only_correctly_identified = set()
none_identified = set()


for file in files:
    actual = file.replace("all_chords/", "").replace(".wav", "").title().replace("-Sharp", "#").replace("-", " ")

    detected_chord_weighted = detect_chord_weighted(file, threshold_float)
    detected_chord_normal = detect_chord_normal(file, threshold_float)

    if detected_chord_weighted == actual and detected_chord_normal == actual:
        both_correctly_identified.add(actual)
    elif detected_chord_weighted == actual:
        weighted_only_correctly_identified.add(actual)
    elif detected_chord_normal == actual:
        normal_only_correctly_identified.add(actual)
    else:
        none_identified.add(actual)

print("both", both_correctly_identified)
print("weighted", weighted_only_correctly_identified)
print("normal", normal_only_correctly_identified)
print("none", none_identified)