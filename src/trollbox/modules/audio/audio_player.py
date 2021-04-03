from sdl2 import SDL_Init, SDL_INIT_AUDIO, SDL_GetError, SDL_Quit, SDL_AUDIO_ALLOW_ANY_CHANGE

from sdl2.sdlmixer import Mix_CloseAudio, MIX_DEFAULT_FORMAT, Mix_GetError, Mix_LoadWAV,\
    Mix_PlayChannel, Mix_Playing, MIX_DEFAULT_CHANNELS, Mix_OpenAudioDevice, Mix_HaltChannel, Mix_AllocateChannels, \
    Mix_Volume

# default is like 8, that won't do :)
CHANNELS = 32


class AudioPlayer:
    def __init__(self, device_name, volume, process_title):
        # NOTE: volume is 0-128
        self.__device_name = device_name
        self.__volume = volume
        self.__files = {}
        self.__process_title = process_title

        self.__sdl_init()
        self.__sdl_open_audio_device()
        self.__sdl_allocate_channels(CHANNELS)
        self.__sdl_set_volume(self.__volume)

    def __del__(self):
        self.__sdl_close()

    def __sdl_init(self):
        if SDL_Init(SDL_INIT_AUDIO) != 0:
            raise RuntimeError("Cannot initialize audio system: {}".format(SDL_GetError()))

    def __sdl_close(self):
        Mix_CloseAudio()
        SDL_Quit(SDL_INIT_AUDIO)

    def __sdl_load_sample(self, filename):
        sample = Mix_LoadWAV(filename)
        if sample is None:
            raise RuntimeError("Unable to load sample: {}".format(filename))
        return sample

    def __sdl_open_audio_device(self):
        device_name_bytes = self.__device_name.encode()
        ret = Mix_OpenAudioDevice(44100, MIX_DEFAULT_FORMAT, MIX_DEFAULT_CHANNELS, 1024,
                                  device_name_bytes, SDL_AUDIO_ALLOW_ANY_CHANGE)
        if ret == -1:
            raise RuntimeError("Cannot open audio device: {}".format(Mix_GetError()))

    def __sdl_allocate_channels(self, channels):
        Mix_AllocateChannels(channels)

    def __sdl_set_volume(self, volume):
        Mix_Volume(-1, volume)

    def __load_file(self, filename):
        sample = self.__sdl_load_sample(filename)
        self.__files[filename] = sample
        return sample

    def play(self, filename_str, callback):
        print("Playing {} on {}, volume: {}".format(filename_str, self.__device_name, self.__volume))
        filename = filename_str.encode()

        sample = self.__files.get(filename)
        if sample is None:
            sample = self.__load_file(filename)

        channel = Mix_PlayChannel(-1, sample, 0)
        if channel == -1:
            err = Mix_GetError()
            # ignore bad audio file errors
            if err != b'Tried to play a NULL chunk' and err != b'No free channels available':
                raise RuntimeError("Cannot play sample {}: {}".format(filename_str, Mix_GetError()))

    def all_done(self):
        num_playing = Mix_Playing(-1)
        print("Channels playing: {}".format(num_playing))
        if num_playing > 0:
            return False
        else:
            return True

    def stop_all(self):
        Mix_HaltChannel(-1)
