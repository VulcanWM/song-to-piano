import soundfile as sf
import numpy as np

def load_audio(file):
    audio, sample_rate = sf.read(file)

    # convert stereo to mono if necessary
    if audio.ndim == 2:
        audio = np.mean(audio, axis=1)

    return audio, sample_rate

def detect_peaks(audio, sample_rate, threshold_float):
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

    return peaks