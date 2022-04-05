import requests
import csv
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
import urllib.request
import requests
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8")

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)#
pd.set_option("display.width", 2000)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

class TSDB:
    with open("TSDB_credentials.txt", "r") as f:
        for details in f:
            username, password, api_key = details.split(":")
    url = "https://www.thesportsdb.com/"
    add = (f"{url}edit_event_add.php?l=4444")
    api = (f"{url}api/v1/json/{api_key}/searchfilename.php?e=")
    login = (f"{url}user_login.php")
    login_data = {"username": username, "password": password}

contents = []

with open(f"links.csv", "r", encoding="UTF-8") as fp:
	lines = csv.reader(fp)
	next(lines, None)
	for line in lines:
		page = urllib.request.Request(f"{line[0]}", headers=headers)
		data = urllib.request.urlopen(page).read()
		soup = BeautifulSoup(data, features="lxml")

		table = soup.find("div", {"class": "InformationBoxTable"})
		keys = [span.get_text() for span in table.find_all("div", {"class": "InformationBoxTitle"})]
		values = [span.contents[0] for span in table.find_all("div", {"class": "InformationBoxContents"})]
		info_dict = dict(zip(keys, values))

		event = info_dict["Name of the event:"]

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
				'date' : date_obj,
				'season' : season,
				'arena' : arena,
				'location' : location,
				'country': country,
				'attendance': attendance,
				'results': res_dict,
				'card': card_dict
		})

df = pd.DataFrame(contents)

df.to_csv(f"test.csv", mode="w", index=False, header=True)
df = pd.read_csv(f"test.csv")

show_dict = {
	'WWE ':'',
	'WWF ':'',
	'Monday Night ':'',
	'Tuesday Night ':'',
	'Wednesday Night ':'',
	'Thursday Night ':'',
	'Friday Night ':'',
	# 'Saturday Night ':'',
	' - Saturday Night':'',
	' 2.0':'',
	' -':'',
	"'":"",
	":":"",
	" (Halle 1)":"",
}

city_dict = {
	'Bagdad' : 'Baghdad',
	'Mailand' : 'Milan'
}

country_dict = {
	' Deutschland': 'Germany',
	' Irak': 'Iraq',
	' Italien': 'Italy',
	' Mexiko': 'Mexico',
	' England, UK':'United Kingdom',
	' Northern Ireland, UK':'United Kingdom',
	' Scotland, UK':'United Kingdom',
	' Wales, UK':'United Kingdom',
	' UK':'United Kingdom',
	' USA':'United States'
}

card_dict = {
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

df = (df
	.replace({"results":card_dict}, regex=True)
	.replace({"card":card_dict}, regex=True)
	.replace({"event":show_dict}, regex=True)
	.replace({"country":country_dict}, regex=True)
	.replace({"location":city_dict}, regex=True)
)

print(df)
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(TSDB.login)

driver.find_element_by_name("username").send_keys(TSDB.username)
driver.find_element_by_name("password").send_keys(TSDB.password)
driver.find_element_by_xpath("/html/body/section/div/div[3]/div/form/div[4]/input").click()

for line in df.itertuples():
    driver.get(TSDB.add)
    driver.find_element_by_name("datepicker").clear();
    driver.find_element_by_name("datepicker").send_keys(str(line.date))
    driver.find_element_by_name("season").send_keys(line.season)
    driver.find_element_by_name("eventcountry").send_keys(line.country)
    if pd.isna(line.location):
        pass
    else:
        driver.find_element_by_name("eventcity").send_keys(line.location)
    driver.find_element_by_name("eventname").send_keys(line.event)
    driver.find_element_by_name("submit").click()
    driver.implicitly_wait(5)

    get_id = driver.find_element_by_link_text("Edit additional event details here").get_attribute('href');
    driver.get(get_id)

    driver.implicitly_wait(5)
    if pd.isna(line.attendance):
        pass
    if line.attendance == 0:
        pass
    else:
        driver.find_element_by_name("attendance").send_keys(str(line.attendance))

    if pd.isna(line.arena):
        pass
    else:
        driver.find_element_by_name("venue").send_keys(line.arena)

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