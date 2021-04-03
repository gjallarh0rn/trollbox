import os

import toga

from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .modules.gui.samples import SampleBox
from .modules.gui.settings import SettingsBox
from .modules.config_manager import ConfigManager
from .modules.audio.audio_manager import AudioManager


BASEDIR = os.path.dirname(__file__)
SOUND_DIR = os.path.join(BASEDIR, "sounds")


class TrollBox(toga.App):
    def __init__(self, name, app_id, config, *args, **kwargs):
        super().__init__(name, app_id, *args, **kwargs)

        self.config = config
        self.sound_dir = SOUND_DIR
        self.audio_manager = AudioManager(self.config)

    def __sound_stopped(self, btn):
        btn.style.color = "RED"

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name, size=(1200, 800))

        container = toga.OptionContainer()

        sample_box = SampleBox(self.config, self.audio_manager, style=Pack(direction=ROW))
        sample_box.reload()

        settings_box = SettingsBox(self.config, self.audio_manager, style=Pack(direction=ROW))

        container.add("Soundboard", sample_box)
        container.add("Settings", settings_box)

        self.main_window.content = container
        self.main_window.show()


def main():
    config = ConfigManager(SOUND_DIR)
    app = TrollBox("Trollbox", "com.troll.box", config)
    app.main_loop()
    config.save_config()


if __name__ == '__main__':
    main()
