import pyaudio
pa = pyaudio.PyAudio()
chosen_device_index = -1
for x in xrange(0,pa.get_device_count()):
    info = pa.get_device_info_by_index(x)
    print pa.get_device_info_by_index(x)
    if info["name"] == "pulse":
        chosen_device_index = info["index"]
        print "\n\n\nChosen index: ", chosen_device_index,"\n\n\n"
print(type(chosen_device_index))
print("\n\n\n Starte Aufnahme")
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input_device_index=chosen_device_index, input=True, output=False)
stream.start_stream()
print("Stoppe Aufnahme")
stream.stop_stream()