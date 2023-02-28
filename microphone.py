import time
import numpy as np
import pyaudio


def start_stream(callback, config):
    p = pyaudio.PyAudio()
    frames_per_buffer = int(config.MIC_RATE / config.FPS)
    stream = p.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=config.MIC_RATE,
                    input=True,
                    frames_per_buffer=frames_per_buffer,
                    input_device_index=config.INPUT_DEVICE_INDEX)
    overflows = 0
    prev_ovf_time = time.time()
    while True:
        try:
            y = (np.fromstring(stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)[0::2])
                 #np.fromstring(stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)[1::2]) / 2
            y = y.astype(np.float32)
            stream.read(stream.get_read_available(), exception_on_overflow=False)
            callback(y)
        except IOError:
            overflows += 1
            if time.time() > prev_ovf_time + 1:
                prev_ovf_time = time.time()
                print('Audio buffer has overflowed {} times'.format(overflows))
    stream.stop_stream()
    stream.close()
    p.terminate()

def list_inputs():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if (device_info.get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", device_info.get('name'), " -  Channels:", device_info.get('maxInputChannels'))