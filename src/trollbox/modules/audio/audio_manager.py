from .audio_subprocess import AudioSubprocess

from .sdl2_layer import get_audio_devices


class AudioManager:
    def __init__(self, config):
        self.__config = config

        self.__audio1 = None
        self.__audio2 = None

        self.__out_name = None
        self.__out_vol = None
        self.__mon_name = None
        self.__mon_vol = None

        self.load_sound_config()

    def load_sound_config(self):
        sound_config = self.__config.get_sound_config()
        if sound_config is not None:
            self.__out_name, self.__mon_name, self.__out_vol, self.__mon_vol = sound_config

            if self.__audio1 is not None:
                print("Shutting down out")
                self.__audio1.shutdown()
                self.__audio1.wait()
            if self.__audio2 is not None:
                print("Shutting down monitor")
                self.__audio2.shutdown()
                self.__audio2.wait()

            self.__audio1 = AudioSubprocess(self.__out_name, self.__out_vol, "Trollbox Master Output")
            self.__audio2 = AudioSubprocess(self.__mon_name, self.__mon_vol, "Trollbox Monitor Output")
            self.__config.update_sound_config(self.__out_name, self.__mon_name, self.__out_vol, self.__mon_vol)

    def __initialized(self):
        if self.__audio1 is not None and self.__audio2 is not None:
            return True
        else:
            return False

    def play_sound(self, name, btn):
        if not self.__initialized():
            print("Sound subsystem is not initialized!")
            return False

        try:
            self.__audio1.play(name)
            self.__audio2.play(name)
        except RuntimeError as exc:
            if exc.args != ("Cannot play sample: b'No free channels available'",):
                raise
        # else:
        #     btn.style.color = "BLUE"

    def stop_all_sound(self, btn):
        if not self.__initialized():
            print("Sound subsystem is not initialized!")
            return False

        self.__audio1.stop_all()
        self.__audio2.stop_all()

    def get_audio_devices(self, is_capture):
        devices = get_audio_devices(is_capture=is_capture)
        return devices
