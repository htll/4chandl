from bs4 import BeautifulSoup
import urllib
import urllib2
import os
from optparse import OptionParser
from time import sleep

def fetchImages(url):
	downloaded_images = []
	#Our user-agent
	user_agent = "Mozzila/6 (Windows 7 64bit) Gecko"
	headers = {"user-agent": user_agent}

	#Request/Response
	request = urllib2.Request(url,None,headers)
	response = urllib2.urlopen(request)
	page = response.read()

	#Parse response into HTMLEntities
	pool = BeautifulSoup(page)

	#Search for all image "links"
	images =  pool.findAll("a",attrs={"class":"fileThumb"})
	for image in images:

		#Append all links to our output list
		downloaded_images.append("http:%s" % image["href"])
	return downloaded_images


def main(url,folder=None,sleep_time=None):
	print "Downloading from",url

	#Check if the folder exists
	if os.path.exists(folder):
		print "Folder exists"
	else:
		print "Createing folder",folder
		os.mkdir(folder)

	#Fetch images
	images = fetchImages(url)
	for dlImage in images:

		#extract the filename by splitting the last /
		filename = dlImage.split("/")[-1:]
		print "Downloading",filename[0]

		#download the image
		urllib.urlretrieve(dlImage,"%s/%s" %(folder,filename[0]))
		
		#if a sleep time was specified then sleep 
		if sleep_time:
			sleep(sleep_time)



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

