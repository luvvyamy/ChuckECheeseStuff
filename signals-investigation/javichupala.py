from scipy.io import wavfile

sampling_rate, data = wavfile.read("chuckeheadmouth.wav")
data = data[1000:, 0]

bits = []

wa = []

last_change = 0
reading = False
reading_counter = 0
anterior = data[0]
for i in range(1, len(data)):
    if (data[last_change] > 0 and data[i] < 0) or (
        data[last_change] < 0 and data[i] > 0
    ):
        if i - last_change < 7:
            if not reading:
                reading = True
                wa.append(i)
            bits.append(1)
        elif reading:
            bits.append(0)
        if reading:
            reading_counter += 1
            if reading_counter == 10:
                reading = False
        last_change = i
    anterior = data[i]

with open("signals_results.txt", "wb") as results_file:
    for i in range(0, len(bits), 8):
        chunk = [0] + bits[i + 1 : i + 8]
        chunk = "".join(map(str, chunk)).zfill(8)
        current_byte = bytes([int(chunk, 2)])
        results_file.write(current_byte)

print("Done!")
print(len(wa))
print(len(bits))
