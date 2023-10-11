import os

from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout
from AudioPlayback import AudioPlayLogic


class ManageAudio(MDBoxLayout):
    def __init__(self, **kwargs):
        super(ManageAudio, self).__init__(**kwargs)
        self.audio_file_location = None
        self.audio_control = None
        self.list_of_audio_files = []  # "1696951878.wave",
        # "1696951952.wave"
        self.directory_path = "."
        self.orientation = 'horizontal'
        self.size_hint = (None, None)
        self.height = 50
        self.width = 200
        md_relative_layout = MDRelativeLayout(size_hint_x=None, width=150)
        self.add_widget(md_relative_layout)
        self.md_icon_button = MDIconButton(
            icon="play",
            theme_text_color="Custom",
            text_color=(0, 0, 1, 1),
            icon_size="30dp",
            pos_hint={"center_y": .5}
        )
        self.md_icon_button.bind(on_press=self.play_audio)
        md_relative_layout.add_widget(self.md_icon_button)
        self.md_progress_bar = ProgressBar(
            size_hint_y=None,
            height="10dp",
            pos_hint={"center_y": .5, "center_x": .9}
        )
        md_relative_layout.add_widget(self.md_progress_bar)

        self.audio_control = AudioPlayLogic(self.md_icon_button, self.md_progress_bar)
        # audio_location=self.list_of_audio_files[0]

    def play_audio(self, instance):
        self.audio_files()
        app = MDApp.get_running_app()
        parent = app.root.ids["box_for_audio_files"]
        button_parent = instance.parent.parent
        if button_parent in parent.children:
            index = parent.children.index(button_parent)
            print(f"Index of button_parent: {index}")
            try:
                self.list_of_audio_files.reverse()
                self.audio_control.audio_name = self.list_of_audio_files[index]
            except Exception as e:
                print(e)

            self.audio_control.toggle_audio_progress()
        else:
            print("button_parent not found in parent.children")

    def audio_files(self):
        try:
            if not os.path.isdir(self.directory_path):
                print(f"Error: {self.directory_path} is not a valid directory.")
                return
            all_files = os.listdir(self.directory_path)
            self.list_of_audio_files = [file for file in all_files if file.lower().endswith('.wave')]


        except Exception as e:
            print(f"An error occurred: {e}")
