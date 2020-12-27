from os import system
from classes.colors import message
from time import sleep

message("Starting update", "green")

youtubedl = ".\\exes\\youtube-dl.exe"
system(f"{youtubedl} -U")

sleep(3)

message("Update finished", "green")