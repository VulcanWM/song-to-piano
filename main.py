import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

audio, sample_rate = sf.read("samples/test.wav")

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
threshold = 0.1 * max(magnitudes)

for i in range(1, len(magnitudes) - 1):
    if (
        magnitudes[i] > magnitudes[i - 1]
        and magnitudes[i] > magnitudes[i + 1]
        and magnitudes[i] > threshold
    ):
        peaks.append(frequencies[i])

print("detected frequencies: ", peaks)

# convert frequency to note
midi_notes = []

for frequency in peaks:
    midi = round(69 + 12 * np.log2(frequency/440))
    midi_notes.append(midi)

print("detected midi notes:", midi_notes)

# detect chord
note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

pitch_classes = {midi % 12 for midi in midi_notes}

for root in range(12):
    major = {(root + interval) % 12 for interval in [0, 4, 7]}
    minor = {(root + interval) % 12 for interval in [0, 3, 7]}

    if pitch_classes == major:
        print("detected chord:", note_names[root], "major")

    if pitch_classes == minor:
        print("detected chord:", note_names[root], "minor")

# # plot the frequency spectrum
# plt.plot(frequencies, magnitudes)
# plt.xlim(0, 1000)
# plt.xlabel("frequency (hz)")
# plt.ylabel("magnitude")
# plt.show()