import os
import sys
import requests
from bs4 import BeautifulSoup as bs
from classes.progress import Progress
from classes.colors import message


class Download:
	def __init__(self, verbose=True, down_format=None, cover=None):
		try:
			if not os.path.exists("downloaded"):
				os.mkdir("downloaded")

			if down_format not in ['mp3', 'wav', 'flac']:
				message(f"Format: {format} not found!", "red")
				exit()

			file = open('data\\links.txt', 'r')
			all_lines = file.readlines()

			if verbose:
				message("Downloading titles", "yellow")

			titles = []
			for line in all_lines:
				site = requests.get(line).text
				soup = bs(site, 'html.parser')
				title = soup.title.text.replace(" - YouTube", '')
				titles.append(title)

			if cover is not None and cover.count("http"):
				image_page = requests.get(cover)
				img_file = open("cover.jpg", 'wb')
				img_file.write(image_page.content)
				img_file.close()

			message("Starting download process", "green")
			prg = Progress(tabs=40, spc="-")

			for i, line in enumerate(all_lines):
				if line.replace("\n", '') != "":
					cur_link = line.split("&list")[0]
					if verbose:
						print(" "*(int(os.get_terminal_size()[0])-1), end='\r')
						perc = float(round(i / len(all_lines), 2))
						suffix = " " + titles[i]
						prg.next(suffix=suffix, cur_perc=perc)
					os.system(f'cd downloaded & .\\..\\exes\\youtube-dl.exe -q -x --audio-format ' + str(down_format) + f' -o "{str(i + 1).zfill(2)} %(title)s.%(ext)s" ' + cur_link)
		except KeyboardInterrupt:
			message("Skipping downloading...", "red")


if __name__ == '__main__':
	try:
		Download(down_format=sys.argv[1])
	except IndexError:
		message("Usage: python down.py <format of files>", "red")
		exit()
