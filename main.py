import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

def detect_chord(file, threshold_float):
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
    threshold = threshold_float * max(magnitudes)

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
    print("detected pitch classes:", pitch_classes)

    for root in range(12):
        major = {(root + interval) % 12 for interval in [0, 4, 7]}
        minor = {(root + interval) % 12 for interval in [0, 3, 7]}

        if major.issubset(pitch_classes):
            print("detected chord:", note_names[root], "Major")
            return note_names[root] + " Major"

        if minor.issubset(pitch_classes):
            print("detected chord:", note_names[root], "Minor")
            return note_names[root] + " Minor"

    return None

total_attempts = 0
correctly_identified = 0
threshold_float = 0.2

print("Threshold:", threshold_float)

files = ["samples/c-major.wav", "samples/c-minor.wav", "samples/f-major.wav", "samples/f-minor.wav", "samples/e-major.wav", "samples/e-minor.wav"]

for file in files:
    actual = file.replace("samples/", "").replace(".wav", "").title().replace("-", " ")
    print("actual:", actual)

    total_attempts += 1
    detected_chord = detect_chord(file, threshold_float)

    if detected_chord is not None and detected_chord == actual:
        correctly_identified += 1

print(f"{total_attempts}/{correctly_identified}")