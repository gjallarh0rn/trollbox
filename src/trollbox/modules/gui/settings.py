import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class SettingsBox(toga.Box):
    def __init__(self, config, audio_manager, *args, **kwargs):
        self.__audio_manager = audio_manager

        self.__config = config
        super(SettingsBox, self).__init__(*args, **kwargs)

        self.__out_name, self.__mon_name, self.__out_vol, self.__mon_vol = None, None, None, None

        self.__refresh_audio_config()

        self.__audio_devices = self.__audio_manager.get_audio_devices(is_capture=False)
        self.__selectable_audio_devices = ["---"] + list(self.__audio_devices.keys())
        # print(self.__selectable_audio_devices, self.__out_name, self.__mon_name, self.__out_vol, self.__mon_vol)

        self.__contentbox = toga.Box(style=Pack(direction=COLUMN))
        self.add(self.__contentbox)

        warning_text =  "Be VERY careful what you set up here!\n"
        warning_text += "Output is the output you wish others to hear (50% volume by default).\n"
        warning_text += "Monitor is for you to hear back what is being played (10% volume by default)\n"

        vbcable_text = "If you only have one sound card, install this: https://vb-audio.com/Cable/"

        self.__warninglabel = toga.Label(warning_text, style=Pack(color="red", padding=10))
        self.__contentbox.add(self.__warninglabel)
        self.__vbcablelabel = toga.Label(vbcable_text, style=Pack(color="blue", padding=10))
        self.__contentbox.add(self.__vbcablelabel)

        sound_out = toga.Box(style=Pack(direction=ROW, width=500))
        self.__contentbox.add(sound_out)
        self.__sound_out = toga.Selection(items=self.__selectable_audio_devices, style=Pack(width=300))
        self.__sound_out.value = self.__out_name if self.__out_name is not None else "---"
        self.__sound_out_volume = toga.Slider(default=self.__out_vol if self.__out_vol is not None else 64, range=(0, 128))
        sound_out.add(toga.Label("Sound Output:"))
        sound_out.add(self.__sound_out)
        sound_out.add(self.__sound_out_volume)

        sound_monitor = toga.Box(style=Pack(direction=ROW, width=500))
        self.__contentbox.add(sound_monitor)
        self.__sound_monitor = toga.Selection(items=self.__selectable_audio_devices, style=Pack(width=300))
        print(self.__mon_name)
        self.__sound_monitor.value = self.__mon_name if self.__mon_name is not None else "---"
        self.__sound_monitor_volume = toga.Slider(default=self.__mon_vol if self.__mon_vol is not None else 13, range=(0, 128))
        sound_monitor.add(toga.Label("Sound Monitor:"))
        sound_monitor.add(self.__sound_monitor)
        sound_monitor.add(self.__sound_monitor_volume)

        self.__save = toga.Button("Save", on_press=self.save, style=Pack(width=200, padding=20))
        self.__contentbox.add(self.__save)

    def __refresh_audio_config(self):
        sound_config = self.__config.get_sound_config()
        if sound_config is not None:
            self.__out_name, self.__mon_name, self.__out_vol, self.__mon_vol = sound_config

    def save(self, *args):
        if self.__sound_out.value == "---" or self.__sound_monitor.value == "---":
            self.window.info_dialog("Error", "Please select a valid device for both output and monitor")
            return

        print("SAVE")
        self.__out_name = self.__sound_out.value
        self.__mon_name = self.__sound_monitor.value
        self.__out_vol = int(self.__sound_out_volume.value)
        self.__mon_vol = int(self.__sound_monitor_volume.value)
        print("Out", self.__out_name, self.__out_vol)
        print("Monitor", self.__mon_name, self.__mon_vol)

        self.__config.update_sound_config(self.__out_name, self.__mon_name, self.__out_vol, self.__mon_vol)
        self.__audio_manager.load_sound_config()

