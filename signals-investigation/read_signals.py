from sys import argv
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy


sampling_rate, data = wavfile.read(argv[1])
data = data[:, 0]

signals_fft = fft(data)
data_freq = fftfreq(len(data), d=1 / sampling_rate)

segment = (1941, 2022)
# print(len(range(*segment)))

bits = []

segment_data = data[1027:]

a = []
b = []

last_value = None
amount_with_no_change = 0
for i in range(len(segment_data)):
    if i != 0:
        if (last_value >= 0 and segment_data[i] >= 0) or (
            last_value < 0 and segment_data[i] < 0
        ):
            amount_with_no_change += 1
        else:
            if amount_with_no_change >= 7.5:
                bits.append(0)
                a.append(amount_with_no_change)
            else:
                bits.append(1)
                b.append(amount_with_no_change)
            amount_with_no_change = 0

    last_value = segment_data[i]

"""for i in range(0, len(segment_data), 10):
    if i != 0:
        if (last_value >= 0 and segment_data[i] >= 0) or (
            last_value < 0 and segment_data[i] < 0
        ):
            bits.append(0)
        else:
            bits.append(1)

    last_value = segment_data[i]"""


count_dollar_percent = 0

with open("signals_results.txt", "wb") as results_file:
    for i in range(0, len(bits), 8):
        chunk = [0] + bits[i + 1 : i + 8]
        chunk = "".join(map(str, chunk)).zfill(8)
        current_byte = bytes([int(chunk, 2)])
        if current_byte == b"\x24" or current_byte == b"\x25":
            count_dollar_percent += 1
            continue
        elif current_byte == b"\x20":
            continue
        if b"\x00" < current_byte < b"\x30":
            continue
        elif current_byte == b"\x00":
            results_file.write(current_byte)
            continue
        if count_dollar_percent < 2:
            if current_byte >= b"\x40":
                if current_byte >= b"\x60":
                    results_file.write(current_byte)
                    pass  # TODO: check what happens here
                else:
                    results_file.write(current_byte)
        else:
            count_dollar_percent = 0
print("Done!")
# print(data[segment[0] : segment[1]])
