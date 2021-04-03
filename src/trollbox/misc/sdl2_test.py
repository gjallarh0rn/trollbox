import time
from multiprocessing import Process

from src import AudioPlayer
from src import AudioSubprocess


def test_playback(device_name, base_dir, filename, volume):
    # NOTE: volume is 0-128
    audio = AudioPlayer(base_dir, device_name, volume, process_title="test")
    audio.play(filename, None)

    while not audio.all_done():
        print("Waiting")
        time.sleep(0.1)
    print("GG")


def test_dual_device_playback(devname1, devname2, filename, vol1, vol2):
    p1 = Process(target=test_playback, args=(devname1, base_dir, filename, vol1))
    p2 = Process(target=test_playback, args=(devname2, base_dir, filename, vol2))
    p1.start()
    time.sleep(0.5)
    p2.start()
    p2.join()


def test_multiprocessing_interface(dev1, dev2, filename, vol1, vol2):
    p1 = AudioSubprocess(dev1, vol1, "test1")
    p2 = AudioSubprocess(dev2, vol2, "test2")
    p1.play(filename)
    p2.play(filename)
    time.sleep(2)
    p1.stop_all()
    p2.stop_all()
    time.sleep(1)
    p1.play(filename)
    p2.play(filename)
    time.sleep(2)
    p1.shutdown()
    p2.shutdown()


if __name__ == "__main__":
    filename = "C:\\Users\\admin\\Music\\soundboard\\loud\\as-loud-as-it-goes.mp3"
    devname1 = "CABLE Input (VB-Audio Virtual Cable)"
    devname2 = "24G2W1G4 (2- NVIDIA High Definition Audio)"

    # test_playback()
    test_multiprocessing_interface(devname1, devname2, filename, 128, 13)
