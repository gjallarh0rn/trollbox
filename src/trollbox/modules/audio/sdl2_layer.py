from sdl2 import SDL_Init, SDL_INIT_AUDIO, SDL_GetError, SDL_GetNumAudioDevices, SDL_GetAudioDeviceName


def get_audio_devices(is_capture):
    devices = {}
    if SDL_Init(SDL_INIT_AUDIO) != 0:
        raise RuntimeError("Cannot initialize audio system: {}".format(SDL_GetError()))

    # iscapture is 0 for playback, 1 for capture
    if is_capture not in (True, False):
        raise ValueError("is_capture")

    iscapture = 0 if not is_capture else 1
    devtype = "playback" if iscapture == 0 else "capture"
    print("{} devices:".format(devtype))

    count = SDL_GetNumAudioDevices(iscapture)
    if count < 0:
        raise RuntimeError("Number of audio devices can't be determined!")

    for j in range(0, count):
        name = SDL_GetAudioDeviceName(j, iscapture)
        if name is None:
            raise RuntimeError("Name couldn't be determined for device {}".format(j))

        name_str = name.decode()
        # print("\t{}: {}".format(j, name_str))
        devices[name_str] = j
    return devices
