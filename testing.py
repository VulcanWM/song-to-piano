from audio_processing import load_audio
from detector import detect_chord_normal, detect_chord_weighted
from pathlib import Path

def detect_single_chords(files, threshold_float):
    both_correctly_identified = set()
    normal_only_correctly_identified = set()
    weighted_only_correctly_identified = set()
    none_identified = set()

    for file in files:
        actual = Path(file).stem.replace("-sharp", "#").replace("-", " ").title()

        audio, sample_rate = load_audio(file)

        detected_chord_weighted = detect_chord_weighted(audio, sample_rate, threshold_float)
        detected_chord_normal = detect_chord_normal(audio, sample_rate, threshold_float)

        if detected_chord_weighted == actual and detected_chord_normal == actual:
            both_correctly_identified.add(actual)
        elif detected_chord_weighted == actual:
            weighted_only_correctly_identified.add(actual)
        elif detected_chord_normal == actual:
            normal_only_correctly_identified.add(actual)
        else:
            none_identified.add(actual)

        # print("both", both_correctly_identified)
        # print("weighted", weighted_only_correctly_identified)
        # print("normal", normal_only_correctly_identified)
        # print("none", none_identified)

    return both_correctly_identified, weighted_only_correctly_identified, normal_only_correctly_identified, none_identified