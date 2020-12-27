from classes.getlinks import GetLinks
from classes.down import Download
from classes.format import Format
from classes.args import Arguments

arg = Arguments()
in_args = arg.getargs()

GetLinks(link=in_args['playlist_link'])
Download(down_format=in_args['format'], cover=in_args['cover'])
Format(args=in_args)
