import threading
import time
from kivy.clock import Clock, mainthread
from kivymd.uix.screen import MDScreen

from AudioLayout import ManageAudio
from AudioRecordingClass import AudioRecorder


class ScreenUI(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenUI, self).__init__(**kwargs)
        self.recording_thread = None
        self.audio_recorder = AudioRecorder()
        self.recording = False
        self.recording_finished = False
        self.audio_list = []

    def recording_safe_thread(self):
        self.recording_thread = threading.Thread(target=self.start_recording)
        self.recording_thread.start()

    def start_recording(self):
        print("Recording thread started.")
        self.audio_recorder.p.terminate()  # Release the PyAudio object
        self.audio_recorder = AudioRecorder()
        self.audio_recorder.name = int(time.time())
        self.audio_recorder.start_recording()
        print("Recording thread finished.")

    def stop_recording(self, *args):
        self.audio_recorder.stop_recording()

    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            # self.recording_safe_thread()
            self.start_recording()
            self.ids.record_button.icon = "stop-circle"
            print("recording....")

        else:
            self.recording = False
            self.stop_recording()
            self.ids.record_button.icon = "record-circle-outline"
            print(f" here is the file name: {self.audio_recorder.name}.wave")
            self.create_audio_layout_object()

    @mainthread
    def create_audio_layout_object(self, *args):
        audio_layout_object = ManageAudio()
        parent = self.ids.box_for_audio_files
        parent.add_widget(audio_layout_object)
