from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
from pathlib import Path
import urllib.request
import requests
import requests
import csv
import re
import io

import sys
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8")

import pandas as pd
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 2000)

class TSDB:
	with open("TSDB_credentials.txt", "r") as f:
		for details in f:
			username, password, api_key = details.split(":")
	url = "https://www.thesportsdb.com/"
	add = f"{url}edit_event_add.php?l="
	api = f"{url}api/v1/json/{api_key}/searchfilename.php?e="
	edit = f"{url}edit_event.php?e="
	login = f"{url}user_login.php"
	login_data = {"username": username, "password": password}

promotion_id_dict = {
	'World Wrestling Entertainment':4444,
	'World Wrestling Federation':4444,
	'All Elite Wrestling':4563,
	'New Japan Pro Wrestling':4449,
	'Pro Wrestling Guerilla':4993,
	'Extreme Championship Wrestling':4451,
	'Pro Wrestling NOAH':4596,
	'All Japan Pro Wrestling':4594,
	'Big Japan Pro-Wrestling':4609,
	'Ring Of Honor':4448,
	'Insane Championship Wrestling':5291,
	'PROGRESS Wrestling':4992,
	'Revolution Pro Wrestling':5290,
	'DDT Pro Wrestling':5289,
	'Westside Xtreme Wrestling':5292,
	'Association les Professionnels du Catch':5292,
	'World Wonder Ring Stardom':5293,
	'Tokyo Joshi Pro-Wrestling':5294,
	'Ice Ribbon':5296,
	'Gatoh Move Pro Wrestling':5295,
	"Sendai Girls' Pro Wrestling":5297,
	'SEAdLINNNG':5298,
	"Marvelous That's Women Pro Wrestling":5298,
	'SHIMMER Women Athletes':5299,
	'Smash Wrestling':5299,
	'GLEAT':4846,
	'Absolute Intense Wrestling':4987,
	'PROGRESS Wrestling':4992,
	'CHIKARA':4988,
	'Game Changer Wrestling':4611,
	'Dragongate Japan Pro-Wrestling':5288,
	'Consejo Mundial De Lucha Libre':4595,
	'Lucha Libre AAA World Wide':4593,
	'World Championship Wrestling':4450,
	'EVOLVE Wrestling':4990,
	'National Wrestling Alliance':4453,
	'Impact Wrestling':4455,
	"All Japan Women's Pro-Wrestling":4705,
	'Lucha Underground':5081,
	'Major League Wrestling':4991,
	'Control Your Narrative':5300,
	'Free The Narrative':5300,
	'Dragon Gate USA':5301,
	'Pro Wrestling FREEDOMS':4697,
	'Active Advance Pro Wrestling':4697,
	'Combat Zone Wrestling':4989,
	'Pro Wrestling Guerrilla':4993,
	'Fighting Of World Japan Pro-Wrestling':4700,
	'WRESTLE-1':4706,
	'Wrestle Association-R':4702,
}

promotion_name_dict = {
	'World Wrestling Entertainment':'WWE',
	'World Wrestling Federation':'WWE',
	'All Elite Wrestling':'AEW',
	'New Japan Pro Wrestling':'NJPW',
	'Extreme Championship Wrestling':'ECW',
	'Pro Wrestling NOAH':'NOAH',
	'All Japan Pro Wrestling':'AJPW',
	'Big Japan Pro-Wrestling':'BJW',
	'Ring Of Honor':'ROH',
	'Insane Championship Wrestling':'ICW',
	'Revolution Pro Wrestling':'RevPro',
	'DDT Pro Wrestling':'DDT Pro',
	'Westside Xtreme Wrestling':'wXw',
	'Association les Professionnels du Catch':'wXw',
	'World Wonder Ring Stardom':'Stardom',
	'Tokyo Joshi Pro-Wrestling':'TJPW',
	'Gatoh Move Pro Wrestling':'Gatoh Move',
	"Sendai Girls' Pro Wrestling":'Sendai Girls',
	"Marvelous That's Women Pro Wrestling":'SEAdLINNNG',
	'SHIMMER Women Athletes':'SHIMMER',
	'Smash Wrestling':'SHIMMER',
	'Dragongate Japan Pro-Wrestling':'Dragon Gate',
	'Absolute Intense Wrestling':'AIW Wrestling',
	'CHIKARA':'CHIKARA Pro',
	'Game Changer Wrestling':'GCW',
	'Consejo Mundial De Lucha Libre':'CMLL',
	'World Championship Wrestling':'WCW',
	'National Wrestling Alliance':'NWA',
	"Major League Wrestling":"MLW",
	"All Japan Women's Pro-Wrestling":"AJW",
	'Control Your Narrative':'CYN',
	'Pro Wrestling FREEDOMS':'FREEDOMS',
	'Fighting Of World Japan Pro-Wrestling':'World Japan',
	'WRESTLE-1':'W-1',
	'Wrestle Association-R':'WAR',
}

show_dict = {
	'WWE ':'',
	'WWF ':'',
	'WCW ':'',
	# 'Monday ':'',
	'GLEAT ':'',
	'AEW/':'',
	'AEW ':'',
	'NJPW Presents ': '',
	'NJPW/':'',
	'NJPW ':'',
	'NJPW/NOAH ': '',
	'NOAH/': '',
	'NOAH ':'',
	'AJW ':'',
	'AAA ':'',
	'CMLL ':'',
	'Impact Wrestling ':'',
	'ROH Wrestling ':'',
	'ROH/':'',
	'ROH ':'',
	'MLW ':'',
	'GCW ':'',
	'CZW ':'',
	'CYN ':'',
	'ICW ':'',
	'WAR ':'',
	'Island ':'WAR Island ',
	'Santo ':'Santo WAR ',
	'Araya ':'Araya WAR ',
	'Winning ':'Winning WAR ',
	'Kitao Dojo/ ':'Kitao Dojo/WAR ',
	'WJ ':'',
	'W-1 ':'',
	'W-1/ZERO1 ':'',
	'WRESTLE-1 ':'',
	'Battle ZERO1 Vs. ':'Battle ZERO1 Vs. W-1 ',
	'W-1/Hiroshi Yamato Produce ':'',
	'W-1/Jiro Kuroshio Produce ':'',
	'Fighting Entertainment ':'',
	'Tour 2020 ':'',
	'Tour 2019 ':'',
	'Tour 2018 ':'',
	'Tour 2017 ':'',
	'Tour 2016 ':'',
	'Tour 2015 ':'',
	'Tour 2014 ':'',
	'Tour 2013 ':'',
	'RevPro/':'',
	'RevPro ':'',
	'Rev Pro ':'',
	'PROGRESS ':'',
	'PWG ':'',
	'DDT x ':'',
	'DDT ':'',
	'DG ': '',
	'Dragon Gate ': '',
	'wXw ':'',
	'APC/':'',
	'Stardom X Stardom':'',
	'Stardom ':'',
	'TJPW ':'',
	" '23":'',
	" '22":'',
	" '21":'',
	" '20":'',
	" '19":'',
	" '18":'',
	" '17":'',
	" '16":'',
	" '15":'',
	" '14":'',
	" '13":'',
	" '12":'',
	" '11":'',
	" '10":'',
	" '09":'',
	" '08":'',
	" '07":'',
	" '06":'',
	" '05":'',
	" '04":'',
	" '03":'',
	" '02":'',
	" '01":'',
	" '00":'',
	" '99":'',
	" '98":'',
	" '97":'',
	" '96":'',
	" '95":'',
	" '94":'',
	" '93":'',
	'Gatoh Move ':'',
	'Sendai Girls ':'',
	'Marvelous/SEAdLINNNG ':'',
	'SHIMMER ':'',
	'SEAdLINNNG ':'',
	'Ice Ribbon New Ice Ribbon ':'New Ice Ribbon ',
	'Ice Ribbon Club Ice Ribbon ':'Club Ice Ribbon ',
	'Ice Ribbon Tax ':'Tax ',
	"Ice Ribbon P's ":'Ps ',
	'FREEDOMS/':'',
	'FREEDOMS ':'',
	'2AW ':'',
	'DGUSA ':'',
	# 'Ice Ribbon ':'',
	# 'New #':'New Ice Ribbon #',
	# 'Club # ':'Club Ice Ribbon #',
	'on Syfy ':'',
	'on Sci Fi ':'',
	' - Saturday Night Dynamite':'',
	' - Friday Night Dynamite':'',
	'SmackDown Live ':'SmackDown ',
	'Super SmackDown ':'SmackDown ',
	'Monday Night ':'',
	'Tuesday Night ':'',
	'Tuesday Nitro':'',
	'Wednesday Night ':'',
	'Thursday Night ':'',
	'Friday Night ':'',
	'Saturday Night ':'',
	' - Tag ': ' - Day ',
	' ~ Live Ergebnisse': '',
	' 2023':'',
	' 2022':'',
	' 2021':'',
	' 2020':'',
	' 2019':'',
	' 2018':'',
	' 2017':'',
	' 2016':'',
	' 2015':'',
	' 2014':'',
	' 2013':'',
	' 2012':'',
	' 2011':'',
	' 2010':'',
	' 2009':'',
	' 2008':'',
	' 2007':'',
	' 2006':'',
	' 2005':'',
	' 2004':'',
	' 2003':'',
	' 2002':'',
	' 2001':'',
	' 2000':'',
	' 1999':'',
	' 1998':'',
	' 1997':'',
	' 1996':'',
	' 1995':'',
	' 1994':'',
	' 1993':'',
	' 1992':'',
	' 1991':'',
	' 1990':'',
	' 2.0':'',
	' -':'',
	"'":"",
	":":"",
	"@ ":"",
	'\\+':' #',
	"&":"and",
	" (Halle 1)":"",
	# "\\s#[0-9]+\\.[0-9]+":"",
	'Lucha Underground ':'',
}

city_dict = {
	'Bagdad' : 'Baghdad',
	'Mailand' : 'Milan',
	'Nanterre ': 'Nanterre, Paris'
}

country_dict = {
	' Deutschland': 'Germany',
	' Frankreich': 'France',
	' Irak': 'Iraq',
	' Italien': 'Italy',
	' Mexiko': 'Mexico',
	' England, UK':'United Kingdom',
	' Northern Ireland, UK':'United Kingdom',
	' Scotland, UK':'United Kingdom',
	' Wales, UK':'United Kingdom',
	' UK':'United Kingdom',
	' USA':'United States',
	'USA':'United States'
}

yt_dict = {
	"https://youtu.be/":"https://www.youtube.com/watch?v=",
	"https://m.youtube.com/watch":"https://www.youtube.com/watch?v=",
}

card_dict = {
	"vakant":"vacant",
    "', '": "\n",
    ", '": "\n",
    "', ": "\n",
    '"': '',
	r"\[\('": "",
	r"'\)]": "",
	r"\[\(": "",
	r"\)]": "",
	r"'\), \('": "\n\n",
	r"'\), \(": "\n\n",
	r"\), \('": "\n\n",
}

def login():
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(TSDB.login)
    driver.find_element_by_name("username").send_keys(TSDB.username)
    driver.find_element_by_name("password").send_keys(TSDB.password)
    driver.find_element_by_xpath("/html/body/section/div/div[3]/div/form/div[4]/input").click()
    return

def scrape():
	contents = []

	with open(f"links.csv", "r", encoding="UTF-8") as fp:
		lines = csv.reader(fp)
		for line in lines:
			try:
				headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
				page = urllib.request.Request(f"{line[0]}", headers=headers)
				data = urllib.request.urlopen(page).read()
				soup = BeautifulSoup(data, features="lxml")

				table = soup.find("div", {"class": "InformationBoxTable"})
				keys = [span.get_text() for span in table.find_all("div", {"class": "InformationBoxTitle"})]
				values = [span.contents[0] for span in table.find_all("div", {"class": "InformationBoxContents"})]
				info_dict = dict(zip(keys, values))

				event = info_dict["Name of the event:"]

				if "Promotion:" in info_dict:
					promotion = info_dict["Promotion:"].get_text()
				else:
					promotion = None
					pass

				if "Arena:" in info_dict:
					arena = info_dict["Arena:"].get_text()
				else:
					arena = None
					pass

				if "Attendance:" in info_dict:
					attendance = info_dict["Attendance:"]
					attendance = attendance.replace(".",",")
				else:
					attendance = None
					pass

				if "Location:" in info_dict:
					location = info_dict["Location:"].get_text()
					if location.count(',') >= 2:
						split_char = ','
						temp = location.split(split_char)
						location, country = split_char.join(temp[:2]), split_char.join(temp[2:])
					else:
						split_char = ','
						temp = location.split(split_char)
						location, country = split_char.join(temp[:1]), split_char.join(temp[1:])
				else:
					location = None
					pass

				if "Broadcast date:" in info_dict:
					date_str = info_dict["Broadcast date:"]
					dd, mm, yy = date_str.split(".")
					date_obj = date(int(yy), int(mm), int(dd))
					season = date_obj.year
				elif "Date:" in info_dict:
					date_str = info_dict["Date:"].get_text()
					dd, mm, yy = date_str.split(".")
					date_obj = date(int(yy), int(mm), int(dd))
					season = date_obj.year

				# pattern = re.compile(r"[a-zA-Z]+:\\./[a-zA-Z]+\\.[a-zA-Z]+\\.[a-zA-Z]+/[a-zA-Z]+\\?v=.*[a-zA-Z]+://([a-zA-Z]+(\\.[a-zA-Z]+)+)/"))
				re1 = re.compile(r"^https://youtu.be/|https://www.youtube.com/watch|https://m.youtube.com/watch|https://www.wrestle-universe.com|https://www.ddtpro.com|https://watch.ddtpro.com|https://live.nicovideo.jp/watch/|https://twitcasting.tv/")

				if "Official video:" in info_dict:
					yt = table.find('a', href=re1)
					yt = yt.get('href')
				else:
					yt = None
					pass

				table = soup.find("div", {"class": "Matches"})
				if table == None:
					res_dict = None
					pass
				else:
					keys = [span.get_text() for span in table.find_all("div", {"class": "MatchType"})]
					values = [span.get_text() for span in table.find_all("div", {"class": "MatchResults"})]
					res_dict = list(zip(keys, values))

				page = urllib.request.Request(f"{line[0]}&page=2", headers=headers)
				data = urllib.request.urlopen(page).read()
				soup = BeautifulSoup(data, features="lxml")

				table = soup.find("div", {"class": "Matches"})
				if table == None:
					card_dict = None
					pass
				else:
					keys = [span.get_text() for span in table.find_all("div", {"class": "MatchType"})]
					values = [span.get_text() for span in table.find_all("div", {"class": "MatchResults"})]
					card_dict = list(zip(keys, values))

				contents.append({
						'cm_id' : line[0].replace("https://www.cagematch.net/?id=1&nr=", ""),
						'event' : event,
						'promotion_id': promotion,
						'promotion_name': promotion,
						'date' : date_obj,
						'season' : season,
						'arena' : arena,
						'location' : location,
						'country': country,
						'attendance': attendance,
						'youtube': yt,
						'results': res_dict,
						'card': card_dict
				})
			except AttributeError:
				print(f"Could not scrape {event}.")
				contents.append({
						'cm_id' : line[0].replace("https://www.cagematch.net/?id=1&nr=", ""),
						'promotion_id': promotion,
						'date' : date_obj,
				})
				df1 = pd.DataFrame(contents)
				file = Path(f"unscraped.csv")
	try:
		df1.to_csv(f"{file}", mode="w", index=False, header=True)
	except:
		pass

	df = pd.DataFrame(contents)
	df.to_csv(f"events.csv", mode="w", index=False, header=True)

	return df

def add_to_TSDB(scrape_bool):
	if scrape_bool == True:
		scrape()
	else:
		pass

	login()

	df = pd.read_csv(f"events.csv")

	df = (df
		.replace({"results":card_dict}, regex=True)
		.replace({"promotion_id":promotion_id_dict}, regex=True)
		.replace({"promotion_name":promotion_name_dict}, regex=True)
		.replace({"card":card_dict}, regex=True)
		.replace({"event":show_dict}, regex=True)
		.replace({"country":country_dict}, regex=True)
		.replace({"youtube":yt_dict}, regex=True)
		.replace({"location":city_dict}, regex=True)
		.replace({"location":country_dict}, regex=True)
	)

	print(df)
	for line in df.itertuples():
		try:
			api_call = requests.get(f"{TSDB.api}{line.promotion_name}_{line.date}_{line.event}")
			storage = api_call.json()
			for event in storage["event"]:
				idEvent = event["idEvent"]
				driver.get(f"{TSDB.edit}{idEvent}")
				if pd.isna(line.card):
					pass
				else:
					driver.find_element_by_name("descriptionEN").clear();
					driver.find_element_by_name("descriptionEN").send_keys(line.card)

				if pd.isna(line.results):
					pass
				else:
					driver.find_element_by_name("result").clear();
					driver.find_element_by_name("result").send_keys(line.results)

					driver.find_element_by_name("submit").click()
		except TypeError:
			driver.get(f"{TSDB.add}{line.promotion_id}")
			driver.find_element_by_name("datepicker").clear();
			driver.find_element_by_name("datepicker").send_keys(str(line.date))
			driver.find_element_by_name("season").send_keys(str(line.season))
			if pd.isna(line.country):
				driver.find_element_by_name("eventcountry").send_keys(line.location)
			else:
				driver.find_element_by_name("eventcountry").send_keys(line.country)

			if pd.isna(line.location):
				pass
			else:
				driver.find_element_by_name("eventcity").send_keys(line.location)

			if pd.isna(line.arena):
				pass
			else:
				driver.find_element_by_name("eventvenue").send_keys(line.arena)
			driver.find_element_by_name("eventname").send_keys(line.event)
			driver.find_element_by_name("submit").click()
			driver.implicitly_wait(5)

			sourcetext = driver.page_source
			searchword = "Event Already Exists"

			if searchword in sourcetext:
				try:
					api_call = requests.get(f"{TSDB.api}{line.promotion_name}_{line.date}_{line.event}")
					storage = api_call.json()
					for event in storage["event"]:
						idEvent = event["idEvent"]
						driver.get(f"{TSDB.edit}{idEvent}")

					if pd.isna(line.attendance):
						pass
					if line.attendance == 0:
						pass
					else:
						driver.find_element_by_name("attendance").clear();
						driver.find_element_by_name("attendance").send_keys(str(line.attendance))

					if pd.isna(line.youtube):
						pass
					else:
						driver.find_element_by_name("video").clear();
						driver.find_element_by_name("video").send_keys(line.youtube)

					if pd.isna(line.card):
						pass
					else:
						driver.find_element_by_name("descriptionEN").clear();
						driver.find_element_by_name("descriptionEN").send_keys(line.card)

					if pd.isna(line.results):
						pass
					else:
						driver.find_element_by_name("result").clear();
						driver.find_element_by_name("result").send_keys(line.results)

					driver.find_element_by_name("submit").click()
				except TypeError:
					print(f"*** {line.event} not found. ***\n")
					pass
			else:
				get_id = driver.find_element_by_link_text("Edit additional event details here").get_attribute('href');
				driver.get(get_id)

				driver.implicitly_wait(5)

				if pd.isna(line.attendance):
					pass
				if line.attendance == 0:
					pass
				else:
					driver.find_element_by_name("attendance").send_keys(str(line.attendance))

				if pd.isna(line.youtube):
					pass
				else:
					driver.find_element_by_name("video").send_keys(line.youtube)

				if pd.isna(line.card):
					pass
				else:
					driver.find_element_by_name("descriptionEN").send_keys(line.card)

				if pd.isna(line.results):
					pass
				else:
					driver.find_element_by_name("result").send_keys(line.results)

				driver.find_element_by_name("submit").click()

	driver.quit()



add_to_TSDB(True)