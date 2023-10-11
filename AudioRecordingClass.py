import pyaudio
import wave


class AudioRecorder:
    def __init__(self, name="output"):
        self.stream = None
        self.name = name
        self.p = pyaudio.PyAudio()
        self.frames = []

    def start_recording(self):
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 44100
        # try:

        self.stream = self.p.open(format=format,
                                  channels=channels,
                                  rate=rate,
                                  input=True,
                                  frames_per_buffer=chunk,
                                  stream_callback=self.on_frame)

        self.frames = []
        print("Recording started.")

    def stop_recording(self):
        print(self.frames[0])
        try:
            if not self.frames:
                print("No audio data to write.")
                return
            self.stream.stop_stream()
            self.stream.close()

            self.p.terminate()

            wf = wave.open(f"{self.name}.wave", 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
            wf.close()

            print(f"Audio recording saved successfully: {self.name}.wave")

        except Exception as e:
            print(f"Error saving audio recording: {e}")

    def on_frame(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return None, pyaudio.paContinue
