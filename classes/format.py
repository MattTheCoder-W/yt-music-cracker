import os
import argparse
from mutagen.flac import FLAC, Picture
from mutagen.mp3 import MP3
from mutagen.id3 import APIC, ID3, TIT2, TALB, TPE1, TCOM, TRCK, ID3NoHeaderError
from classes.colors import message


class Format:
    def __init__(self, args):
        if args['cover'] is not None and args['cover'].count("http"):
            args['cover'] = "cover.jpg"

        # Check for necessary folders...
        if not os.path.exists("backup"):
            os.mkdir("backup")

        working_formats = ['mp3', 'flac']
        track_index = 0

        for filename in os.listdir("downloaded/"):
            # check for file types that script is not interested in and skip them
            if filename.split('.')[-1] in working_formats and filename:
                ext = filename.split(".")[-1]
                file_location = f'downloaded\\{filename}'
                file_no_ext = '.'.join(filename.split('.')[:-1])  # Filename with no file ext.

                artist = args['artist']
                try:
                    title = file_no_ext.split(' - ')[1]
                except IndexError:
                    title = file_no_ext[3:]

                # Skip specified phrases in title
                if args['skip'] is not None:
                    if " && " in args['skip']:  # If there is multiple phrases to skip
                        skips = args['skip'].split(" && ")
                        for skip in skips:
                            if skip in title:
                                title = title.replace(skip, '')
                    elif args['skip'] in title:  # If there is only one phrase to skip
                        title = title.replace(args['skip'], '')

                # Backup all files in working folder
                os.system(f'copy "{file_location}" backup\\ > nul')

                # Message showing some dev data to help debug
                message(f'Saving: {artist} - {title}.{ext}', "green")

                if ext == "flac":
                    audio = FLAC(file_location)

                    audio['title'] = title
                    audio['album'] = args['album_title']
                    audio['album_artist'] = artist
                    audio['artist'] = artist
                    audio['tracknumber'] = str(track_index + 1)
                elif ext == "mp3":
                    try:
                        audio = MP3(file_location, ID3=ID3)
                    except ID3NoHeaderError:
                        print("Adding ID3 header")
                        audio = MP3(ID3=ID3)
                    audio['TIT2'] = TIT2(encoding=3, text=title)  # Set title
                    audio["TALB"] = TALB(encoding=3, text=args['album_title'])  # Set Album
                    audio["TPE1"] = TPE1(encoding=3, text=artist)  # Set Artist
                    audio["TCOM"] = TCOM(encoding=3, text=artist)  # Set Artist 2
                    audio["TRCK"] = TRCK(encoding=3, text=str(track_index + 1))  # Set track number
                else:
                    audio = None
                    message("Only FLAC and MP3 formats are allowed!", "red")
                    exit()

                if args['cover'] is not None:
                    # Add album cover for given format
                    if ext == "flac":
                        audio.add_picture(self.add_picture(args['cover']))
                    elif ext == "mp3":
                        if args['cover'].split('.')[-1] == "jpg":
                            mime = "image/jpeg"
                        else:
                            mime = "image/png"
                        audio.tags.add(APIC(mime=mime, type=3, desc=u'Cover', data=open(args['cover'], 'rb').read()))

                audio.save(file_location)

                # Rename current file
                command = f'rename "{file_location}" "{str(track_index + 1).zfill(2)} {artist} - {title}.{ext}"'
                os.system(command)

                track_index += 1  # Move to next track index (number)
            else:
                message(f"Skipping {filename}", "red")

        message("Deleting backup files...", "yellow")
        os.system('del backup\\*')
        os.rmdir("backup")

    @staticmethod
    def add_picture(pic):
        image = Picture()
        image.type = 3
        if pic.split('.')[-1] in ["jpg", "jpeg"]:
            image.mime = "image/jpeg"
        else:
            image.mime = "image/png"
        image.desc = 'front cover'
        with open(pic, 'rb') as album:
            image.data = album.read()
        return image


if __name__ == "__main__":
    print("Note:\n\tAll music files should be in format:\n\t\t%num% %artist% - %title%.mp3")
    print()

    ap = argparse.ArgumentParser()
    ap.add_argument('artist', type=str, help="Artist of songs")
    ap.add_argument('album', type=str, help="Album of songs")

    ap.add_argument('-c', '--cover', type=str, help="Cover img file for songs")
    ap.add_argument('-s', '--skip', type=str,
                    help="Phrase to skip in titles of songs, if you want to skip more than one, use ' && ' separator "
                         "between them.")
    ap.add_argument('-tn', '--track-only', action="store_true", help="Filename contains only track name.")
    ap.add_argument('-p', '--prefix', type=str, help="Prefix for output files")
    in_args = vars(ap.parse_args())
    Format(in_args)