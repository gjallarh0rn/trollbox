from multiprocessing import Process, Queue

from .audio_player import AudioPlayer


class AudioSubprocess:
    def __init__(self, devname, volume, process_title):
        self.__devname = devname
        self.__volume = volume
        self.__process_title = process_title

        self.__inq = Queue()
        self.__outq = Queue()
        self.__p = Process(target=self.spawn_subprocess, daemon=True)
        self.__p.start()

    def spawn_subprocess(self):
        audio = AudioPlayer(self.__devname, self.__volume, self.__process_title)

        while True:
            cmd = self.__inq.get()
            cmdname, cmdparam = cmd
            if cmdname == "play":
                audio.play(cmdparam, None)
            elif cmdname == "stop_all":
                audio.stop_all()
            elif cmdname == "shutdown":
                break
            else:
                raise ValueError("Unknown command: {}".format(cmdname))

    def play(self, filename):
        self.__inq.put(("play", filename))

    def stop_all(self):
        self.__inq.put(("stop_all", None))

    def shutdown(self):
        self.__inq.put(("shutdown", None))

    def wait(self):
        while not self.__outq.empty():
            print(self.__outq.get_nowait())
