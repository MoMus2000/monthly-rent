import requests 
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import os
import sys

title= []
desc= []
time = []
add = []
links =[]
prices = []
locations = []

output = pd.DataFrame()

if len(sys.argv) > 0:
	limit = sys.argv[1]

else:
	limit = 1000

for i in tqdm(range(1,int(limit))):
	try:
		url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/1+bedroom-apartment"+str(i)+"/c37l1700273a27949001a29276001?ll=43.795524%2C-79.425361&address=15+Tangreen+Ct%2C+North+York%2C+ON+M2M+3Z2%2C+Canada&keywordToAttribute=1+bedroom+apartment&radius=18.0"
		x = requests.get(url,timeout=30)
		soup = BeautifulSoup(x.text, 'html.parser')
		info_container = soup.findAll("div", class_="info-container")
		description = soup.findAll("div",class_="description")
		price = soup.findAll("div",class_="price")
		location = soup.findAll("div",class_="location")
		for i in info_container:
			urls = i.find('a')['href']
			links.append("https://www.kijiji.ca"+urls)
			titles = i.find('div',class_="title").text.strip()
			title.append(titles)
		for p in price:
			strs = ''.join(p.text.split())
			prices.append(strs)

		for d in description:
			strs = ' '.join(d.text.split())
			desc.append(strs)
		for l in location:
			locs = l.find('span')
			strs = ' '.join(locs.text.split())
			locations.append(strs)
	except Exception as e:
		print(e)
		break

output["Title"] = title
output["Location"] = locations
output["Price"] = prices
output["description"] = desc
output["Links"] = links

now = datetime.now()

output.to_csv(str(os.getcwd())+"/"+now.strftime("%Y-%m-%d %H:%M:%S")+".csv")


