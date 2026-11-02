from detector import detect_chord_weighted
from audio_processing import load_audio

def detect_chord_progression(file, threshold_float, window_duration=0.5, hop_duration=0.25):
    audio, sample_rate = load_audio(file)

    window_size = int(window_duration * sample_rate)
    hop_size = int(hop_duration * sample_rate)

    results = []
    for start in range(0, len(audio) - window_size + 1, hop_size):
        segment = audio[start:start + window_size]

        chord = detect_chord_weighted(segment, sample_rate, threshold_float)

        time = start / sample_rate
        results.append((time, chord))

    return results
