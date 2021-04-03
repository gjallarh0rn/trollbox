import os
import functools

import toga
import keyboard

from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class HotkeyBox(toga.Box):
    def __init__(self, full_name, audio_manager, config, *args, **kwargs):
        self.__full_name = full_name
        self.__audio_manager = audio_manager
        self.__config = config
        super(HotkeyBox, self).__init__(*args, **kwargs)

        _, name = os.path.split(full_name)
        short_name = name[:20]

        self.__hotkey = None
        self.__button = toga.Button(short_name,
                                    style=Pack(width=150),
                                    on_press=functools.partial(self.__audio_manager.play_sound, self.__full_name))
        self.add(self.__button)

        self.__hotkey_button = toga.Button("...", on_press=self.add_hotkey, style=Pack(width=50))
        self.add(self.__hotkey_button)

        self.__hotkey = self.__config.get_hotkey(self.__full_name)
        if self.__hotkey is not None:
            self.__hotkey_button.label = self.__hotkey
            keyboard.on_press_key(self.__hotkey, self.__button.on_press, suppress=True)

    def add_hotkey(self, btn):
        k = keyboard.read_key()
        if k == "esc":
            btn.label = "..."
            keyboard.unhook(self.__hotkey)
            self.__hotkey = None
            self.__config.set_hotkey(self.__full_name, None)
        elif k.lower() == "f12":
            self.window.info_dialog("Error", "Not allowed to set F12 as hotkey")
            btn.label = "..."
            self.__hotkey = None
            self.__config.set_hotkey(self.__full_name, None)
        else:
            btn.label = k
            self.__hotkey = k
            keyboard.on_press_key(self.__hotkey, self.__button.on_press, suppress=True)
            self.__config.set_hotkey(self.__full_name, self.__hotkey)
