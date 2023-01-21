from bs4 import BeautifulSoup
import requests
import os.path
import os
from optparse import OptionParser
from time import sleep

def fetchImages(url):
	downloaded_images = []
	#Our user-agent
	user_agent = "Mozzila/9 (Windows 10 64bit) Gecko"
	headers = {"user-agent": user_agent}

	#Request/Response
	request = requests.get(url,allow_redirects=True,headers=headers)
	if request.status_code != 200:
		return
	else:
		#Parse response into HTMLEntities
		pool = BeautifulSoup(request.text)

		#Search for all image "links"
		images =  pool.select("a[class=fileThumb]")
		for image in images:
			href = image.attrs['href']
			print(f"Found {href}")
			#Append all links to our output list
			downloaded_images.append(f"http:{href}")
	return downloaded_images

def save_file(url, output_folder, filename):
	print(f"Downloading {filename}")
	with open(f"{output_folder}/{filename}","wb") as ifile:
		r_image = requests.get(url)
		ifile.write(r_image.content)


def main(url,folder=None,sleep_time=None):
	print(f"Attempting to download from {url}")

	#Check if the folder exists
	if os.path.exists(folder):
		print(f"Folder {folder} exists")
	else:
		print(f"Createing folder {folder}")
		os.mkdir(folder)

	#Fetch images
	images = fetchImages(url)
	for index,item in enumerate(images):

		#extract the filename by splitting the last /
		filename = item.split("/")[-1:][0]

		print(f"Item {index}/{len(images)}")
		#download the image
		save_file(item,folder,filename)

		#if a sleep time was specified then sleep
		try:
			if sleep_time:
				sleep(sleep_time)
		except KeyboardInterrupt:
			break



if __name__ == "__main__":
	usage = "Usage: %prog [Options] thread_url"
	desc = "Downloads all images from a 4chan thread"
	parser = OptionParser(usage=usage,description=desc)
	parser.add_option("-f","--folder",default=".",dest="outfolder",help="Location where to download images")
	parser.add_option("-s","--sleep",default=2,dest="sleeptimer",help="How long to wait between each image download")
	(options,args) = parser.parse_args()
	if(len(args) > 0):
		url = args[0]
		folder = options.outfolder
		sleep_time = options.sleeptimer
		main(url,folder,sleep_time)
	else:
		parser.print_help()

