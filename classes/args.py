import argparse
from classes.interactive import Interactive
from classes.colors import message


class Arguments:
    def __init__(self):
        ap = argparse.ArgumentParser()
        ap.add_argument('-i', '--interactive', action="store_true", help="Interactive mode of this script")
        ap.add_argument('-p', '--playlist-link', type=str, help='Link for playlist on youtube')
        ap.add_argument('-f', '--format', type=str, help='File format (flac/mp3)')
        ap.add_argument('-a', '--artist', type=str, help='Artist of album')
        ap.add_argument('-t', '--album-title', type=str, help='Title of the album')
        ap.add_argument('-c', '--cover', type=str, help='Cover image file or link to online cover')
        ap.add_argument('-s', '--skip', type=str, help='Phrase to skip in titles of songs, if you want to skip more than one, use " && " separator between them.')
        self.args = ap.parse_args()
        self.interactive = self.args.interactive
        self.args = vars(self.args)
        if self.interactive:
            args = Interactive().getargs()
            self.args = args
        elif self.args['format'] not in ['flac', 'mp3']:
            message(f"Format {self.args['format']} not found!", "red")
            exit()


    def getargs(self):
        return self.args
