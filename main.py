from testing import detect_single_chords
from pathlib import Path

if __name__ == "__main__":
    threshold_float = 0.05

    files = sorted(Path("all_chords").glob("*.wav"))

    both, weighted, normal, none = detect_single_chords(files, threshold_float)

    total = len(files)

    print("Threshold:", threshold_float)
    print(f"Normal: {len(both) + len(normal)}/{total}")
    print(f"Weighted: {len(both) + len(weighted)}/{total}")

    print("Both:", both)
    print("Weighted only:", weighted)
    print("Normal only:", normal)
    print("None:", none)