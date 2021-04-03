import os
import re

import requests


def download_sounds_from_website(basedir):
    baseurl = "https://www.myinstants.com"
    r = requests.get(baseurl + "/search/?name=Loud")
    r.raise_for_status()

    print("[+] Downloading file list")
    soundfiles = []
    for match in re.findall("onmousedown=\"play\('(?P<filename>.*?)'\)\">", r.text):
        fileurl = baseurl + match
        soundfiles.append(fileurl)

    print("[+] File list found, {} soundfiles detected".format(len(soundfiles)))
    for fileurl in soundfiles:
        filename = fileurl.split("/")[-1]
        print("[?] Is file url cached locally?")
        fullpath = os.path.join(basedir, filename)
        if os.path.exists(fullpath):
            print("  [+] File {} is cached locally".format(fullpath))
            continue

        print("  [+] Downloading {}".format(fileurl))
        r = requests.get(fileurl)
        r.raise_for_status()
        with open(fullpath, "wb") as f:
            f.write(r.content)
        print("  [+] File {} saved".format(fullpath))

    print("[+] Done")


if __name__ == "__main__":
    download_sounds_from_website("./sounds/loud/")
