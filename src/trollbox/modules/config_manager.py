import os
import json

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".trollbox", "config.json")


class ConfigManager:
    def __init__(self, default_sound_dir):
        self.__default_sound_dir = default_sound_dir

        self.__sounds = set()
        self.__hotkeys = {}
        self.__sound_config = None

        self.__load_config()
        if len(self.__sounds) == 0:
            self.load_from_directory(self.__default_sound_dir)

    def __load_config(self):
        print("Trying to load config", CONFIG_FILE)
        if os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as conf:
                config = json.load(conf)
            if config is not None:
                self.__hotkeys = config["hotkeys"]
                self.__sounds = set(config["sounds"])
                self.__sound_config = config["sound_config"]

    def save_config(self, *args):
        print("Saving config")
        config = {
            "sounds": list(self.__sounds),
            "hotkeys": self.__hotkeys,
            "sound_config": self.__sound_config
        }
        data = json.dumps(config)

        dirname = os.path.dirname(CONFIG_FILE)
        os.makedirs(dirname, exist_ok=True)
        with open(CONFIG_FILE, "wt") as conf:
            conf.write(data)

    def delete_config(self, *args):
        print("Config file deleted")
        os.unlink(CONFIG_FILE)

    def list_sounds(self):
        return sorted(list(self.__sounds))

    def load_from_directory(self, path):
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                filename = os.path.join(dirpath, file)
                if filename.endswith(".mp3"):
                    self.__sounds.add(filename)

    def set_hotkey(self, filename, hotkey):
        if hotkey is None:
            self.__hotkeys.pop(hotkey, None)
        else:
            self.__hotkeys[filename] = hotkey

    def get_hotkey(self, filename):
        if filename in self.__hotkeys:
            return self.__hotkeys[filename]

    def get_sound_config(self):
        if self.__sound_config is None:
            return None

        c = self.__sound_config
        return c["out_name"], c["mon_name"], c["out_vol"], c["mon_vol"]

    def update_sound_config(self, out_name, mon_name, out_vol, mon_vol):
        self.__sound_config = {
            "out_name": out_name,
            "mon_name": mon_name,
            "out_vol": out_vol,
            "mon_vol": mon_vol
        }
