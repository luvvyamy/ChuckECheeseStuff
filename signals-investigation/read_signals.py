from sys import argv
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
import scipy.signal
import matplotlib.pyplot as plt
import numpy


sampling_rate, data = wavfile.read(argv[1])
data = data[:, 0]
data = data / numpy.max(numpy.abs(data))
# data = numpy.gradient(data)
print(data[1245:1265])
data_peaks = []
data_peaks += set(scipy.signal.find_peaks(data, 5000)[0])
wa = [data[i] for i in data_peaks]
print(numpy.min(wa))
data_peaks += set(scipy.signal.find_peaks(data, -5000)[0])
wa = [data[i] for i in data_peaks]
print(numpy.min(wa))
print(numpy.max(wa))
data_peaks.sort()

segment = (1941, 2022)
# print(len(range(*segment)))

bits = []
bits_2 = []

segment_data = data

a = []
b = []

last_value = None
amount_with_no_change = 0

plt.title("Line graph")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.plot(range(len(data[:50])), data[:50], color="red")
plt.show()


def transitions_to_bits(transitions, sample_rate, bit_rate):
    bit_period = sample_rate / bit_rate
    bits = []
    last_transition = transitions[0]
    for transition in transitions[1:]:
        time_interval = (transition - last_transition) / sample_rate
        if time_interval >= bit_period / 2:
            bits.append(1 if time_interval < bit_period else 0)
        last_transition = transition
    return bits


bits = transitions_to_bits(data_peaks, 9)

with open("signals_results.txt", "wb") as results_file:
    for i in range(0, len(bits), 8):
        chunk = bits[i : i + 8]
        chunk = "".join(map(str, chunk)).zfill(8)
        current_byte = bytes([int(chunk, 2) & 0x7F])
        results_file.write(current_byte)
print("Done!")
