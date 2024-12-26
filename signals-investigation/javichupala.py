from scipy.io import wavfile
import sys
import os.path
import numpy as np

file_path = sys.argv[1]
filename = os.path.basename(file_path).split(".")[0]

sampling_rate, data = wavfile.read(file_path)
data = data[1024:, 0]

bits = []
polarity_changes = np.where(np.diff(np.signbit(data)))[0]

reading_counter = 0
ignore_next_polar = False
for i in range(1, len(polarity_changes)):
    if ignore_next_polar:
        ignore_next_polar = False
        continue

    if polarity_changes[i] - polarity_changes[i - 1] >= 7:
        if reading_counter > 0:
            bits.append(0)
            reading_counter += 1
    else:
        bits.append(1)
        reading_counter += 1
        ignore_next_polar = True

    if reading_counter >= 9:
        reading_counter = 0

    print(f"{100 * i/len(polarity_changes)}% processed...")

print("Writing to file...")
with open(f"signals_results_{filename}.txt", "wb") as results_file:
    for i in range(0, len(bits), 9):
        if len(bits) - i < 9:
            break
        """if ja % 2 == 1:
        xd = bits[i + 1 : i + 8]
        for j in range(1, 8):
            bits[i + j] = xd[-j]"""
        chunk = bits[i + 1 : i + 9]
        chunk.reverse()
        for j in range(8):
            chunk[j] = 1 if chunk[j] == 0 else 0
        chunk = "".join(map(str, chunk)).zfill(8)
        print(chunk, end=" ")
        current_byte = bytes([int(chunk, 2)])
        results_file.write(current_byte)

print("Done!")
