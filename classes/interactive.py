from classes.colors import message
from os import system
from os import get_terminal_size


def showbanner(file, size, line=False):
    width = list(get_terminal_size())[0]
    bannerwidth = size
    center = int((width - bannerwidth) / 2)
    if center < 0:
        center = 0
    with open(file, "rb") as f:
        for line in f.readlines():
            print(" "*center + line.decode().replace('\n', ''))
    if line:
        print(" "*center + "="*bannerwidth)


class Interactive:
    def __init__(self):
        system("cls")
        self.args = {'playlist_link': '', 'format': '', 'artist': '', 'album_title': '', 'cover': '', 'skip': None}
        showbanner("data/banner.txt", 63, line=True)
        message("Playlist link: ", "blue", end="")
        self.args['playlist_link'] = str(input())
        message("Artist: ", "blue", end="")
        self.args['artist'] = str(input())
        message("Album Title: ", "blue", end="")
        self.args['album_title'] = str(input())
        while True:
            message("Files format(flac/mp3): ", "blue", end="")
            self.args['format'] = str(input())
            if self.args['format'] not in ['flac', 'mp3']:
                message("Please specify correct file format!", "red")
                continue
            break
        while True:
            message("Cover image(Empty for none): ", "blue", end="")
            self.args['cover'] = str(input())
            if self.args['cover'].count(".") == 0:
                message("Please specify correct file or link!", "red")
                continue
            if self.args['cover'] == "":
                self.args['cover'] = None
            break
        message("Phrases to skip in titles(Empty for none): ", "blue", end="")
        self.args['skip'] = str(input())
        if self.args['skip'] == "":
            self.args['skip'] = None

    def getargs(self):
        system("cls")
        showbanner("data/banner2.txt", 37)
        return self.args
