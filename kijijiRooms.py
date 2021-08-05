import requests 
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import os

title= []
desc= []
time = []
add = []
links =[]
prices = []
locations = []

output = pd.DataFrame()
while True:
	try:
		limit = input("How many pages to scrape ....? ")
		if(int(limit)<2):
			raise Exception("Sorry 2 is the least ...")
		else:
			break
	except Exception as e:
		print(e)
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


from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib


def send_mail():
    # Create a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText(MESSAGE_BODY, 'plain')
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    # Add body to email
    msg.attach(body_part)
    # open and read the CSV file in binary
    with open(PATH_TO_CSV_FILE,'rb') as file:
    # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name=FILE_NAME))

    # Create SMTP object
    smtp_obj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    # Login to the server
    smtp_obj.login(SMTP_USERNAME, SMTP_PASSWORD)

    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()