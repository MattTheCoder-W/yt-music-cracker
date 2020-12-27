from lxml import html
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import argparse
import os
from classes.colors import message


class GetLinks:
	def __init__(self, link):
		try:
			message("Downloading playlist data", "yellow")

			options = Options()
			options.headless = True
			driver = webdriver.Firefox(options=options, executable_path=r'exes/geckodriver.exe', service_log_path=os.path.devnull)
			driver.get(link)

			html_site = driver.page_source

			driver.quit()

			message("Finding necessary elements", "yellow")
			tree = html.fromstring(html_site)
			buyers = tree.xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-playlist-video-list-renderer')
			soup = bs(html.tostring(buyers[0]), 'html.parser')
			list_of_vids = soup.find("div", attrs={"id": "contents", "class": "style-scope ytd-playlist-video-list-renderer"})
			elements_of_list = list_of_vids.findAll('ytd-playlist-video-renderer')

			message("Processing data", "green")
			links = []
			for elem in elements_of_list:
				content = elem.find("div", attrs={"id": "content"})
				cur_link_element = content.find("a", attrs={"class": "yt-simple-endpoint"})
				cur_link = cur_link_element['href']
				vid_id = cur_link.split("&")[0]
				cur_link = "https://www.youtube.com" + vid_id
				links.append(cur_link)

			message("Saving data", "yellow")
			with open("data/links.txt", "w") as f:
				for link in links:
					f.write(link + "\n")

			message("Done!", "green")
		except KeyboardInterrupt:
			message("Skipping...", "red")


if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument('list_link', type=str, help="Link to playlist on youtube")
	args = vars(ap.parse_args())
	GetLinks(args['list_link'])
