import threading
import wave
import pyaudio
from kivy.clock import Clock


class AudioPlayLogic:
    def __init__(self, button, progress_bar, audio_location=None):
        self.button = button
        self.progress_bar = progress_bar
        self.audio_name = audio_location
        self.play_audio_flag = None
        self.progress_running = False
        self.schedule_event = None
        self.audio_thread = None
        self.playback_position = 0
        self.bar_position = 0
        self.frame_rate = 0
        self.schedule_object = Clock.schedule_interval(self.initialize_audio_params, 1)
        print(f"this is the audio location from its class {self.audio_name}")

    def initialize_audio_params(self, *args):
        if self.audio_name:
            print("Audio file exist!", self.audio_name)
            self.schedule_object.cancel()
            p = pyaudio.PyAudio()
            wf = wave.open(self.audio_name, 'rb')
            self.frame_rate = wf.getnframes() / wf.getframerate()
            wf.close()
            p.terminate()
        else:
            print("Audio file doesnt exist!")

    def toggle_audio_progress(self, *args):
        button = self.button
        if self.frame_rate != 0:
            if self.play_audio_flag:
                self.stop_audio()
                self.stop_update_progress()
                button.icon = "play"
            else:
                self.start_audio()
                self.start_update_progress()
                button.icon = "stop-circle"
                print("inside the toggle bar ")

    def advance_the_progress_bar(self, *args):
        button = self.button
        instance = self.progress_bar
        instance.value += 1
        if instance.value >= 100:
            instance.value = 0
            button.icon = "play"
            self.schedule_event.cancel()
            self.progress_running = not self.progress_running

    def stop_update_progress(self):
        if self.schedule_event:
            self.schedule_event.cancel()
        self.progress_running = False

    def play_audio(self):
        if self.audio_name:
            p = pyaudio.PyAudio()
            wf = wave.open(self.audio_name, 'rb')
            print(f" this is audio file from the play function {self.audio_name}")
            wf.setpos(self.playback_position)
            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )

            data = wf.readframes(1024)

            while data and self.play_audio_flag:
                stream.write(data)
                data = wf.readframes(1024)
                if wf.tell() == wf.getnframes():
                    wf.setpos(0)
                    self.playback_position = 0
                    self.play_audio_flag = False
                    break

            self.playback_position = wf.tell()

            stream.stop_stream()
            stream.close()
            p.terminate()

    def start_update_progress(self):
        if self.progress_running:
            return
        if self.frame_rate:
            self.schedule_event = Clock.schedule_interval(self.advance_the_progress_bar, self.frame_rate / 90.0)
            print(f"this is the total duration: {self.frame_rate}")
            self.progress_running = True
        else:
            print("Audio frame doesnt exist!")

    # I think the issue is related to the treading

    def start_audio(self):
        if self.audio_thread is None or not self.audio_thread.is_alive():
            self.play_audio_flag = True
            self.audio_thread = threading.Thread(target=self.play_audio)
            self.audio_thread.start()

    def stop_audio(self):
        self.play_audio_flag = False
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join()
