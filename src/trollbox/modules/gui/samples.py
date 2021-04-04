import os
import toga
import keyboard

from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .hotkey import HotkeyBox


BOX_SIZE = 30


class SampleBox(toga.Box):
    def __init__(self, config, audio_manager, *args, **kwargs):
        self.__config = config
        self.__audio_manager = audio_manager
        super(SampleBox, self).__init__(*args, **kwargs)

        self.__controlbox = toga.Box(style=Pack(direction=COLUMN, width=150))
        # self.__controlbox.add(toga.Button("Load files", on_press=self.load_files))
        self.__controlbox.add(toga.Button("Open trollbox sound folder", on_press=self.open_sound_folder))
        self.__controlbox.add(toga.Button("Load files from trollbox", on_press=self.load_files_trollbox))
        # self.__controlbox.add(toga.Button("DBG: Refresh", on_press=self.reload))
        # self.__controlbox.add(toga.Button("DBG: Save config", on_press=self.__config.save_config))

        stop_all = toga.Button('STOP ALL SOUNDS [F12]', style=Pack(color="red"),
                               on_press=self.__audio_manager.stop_all_sound)
        self.__controlbox.add(stop_all)
        keyboard.on_press_key('F12', stop_all.on_press, suppress=True)

        self.add(self.__controlbox)

        self.__contentbox = toga.Box(style=Pack(direction=ROW))
        self.add(self.__contentbox)

    def open_sound_folder(self, *args):
        os.startfile(self.window.app.sound_dir)

    def load_files_trollbox(self, *args):
        self.__config.load_from_directory(self.window.app.sound_dir)
        self.reload()

    def load_files(self, *args):
        sound_dir = self.window.app.sound_dir
        try:
            paths = self.window.select_folder_dialog(
                title="Select folder with Toga",
                initial_directory=sound_dir
            )
        except ValueError:
            return
        else:
            path = paths[0]
            print("Folder selected:", path)
            self.__config.load_from_directory(path)
            self.reload()

    def reload(self, *args):
        # clear the box
        # TODO: for some reason we have to do this in a loop. what the hell!?
        while True:
            children = self.__contentbox.children
            if len(children) == 0:
                break
            for child in children:
                print("Removing child", child)
                self.__contentbox.remove(child)

        samples_box = toga.Box(style=Pack(direction=COLUMN))
        self.__contentbox.add(samples_box)

        total = 0
        for full_name in self.__config.list_sounds():
            if total % BOX_SIZE == 0 and total != 0:
                samples_box = toga.Box(style=Pack(direction=COLUMN))
                self.__contentbox.add(samples_box)
            total += 1

            sample_box = HotkeyBox(full_name, self.__audio_manager, self.__config)
            samples_box.add(sample_box)

