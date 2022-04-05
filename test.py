import  pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from pathlib import Path
import re
import datetime
import requests
import csv
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8")

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)#
pd.set_option("display.width", 2000)

class TSDB:
    with open("TSDB_credentials.txt", "r") as f:
        for details in f:
            username, password, api_key = details.split(":")
    url = "https://www.thesportsdb.com/"
    add = (f"{url}edit_event_add.php?l=4444")
    api = (f"{url}api/v1/json/{api_key}/searchfilename.php?e=")
    login = (f"{url}user_login.php")
    login_data = {"username": username, "password": password}

df = pd.read_csv('test.csv')

show_dict = {
	'WWE ':'',
	'WWF ':'',
	'Monday Night ':'',
	'Tuesday Night ':'',
	'Wednesday Night ':'',
	'Thursday Night ':'',
	'Friday Night ':'',
	'Saturday Night ':'',
	' - Saturday Night':'',
	' -':'',
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
df.to_csv(f"test1.csv", mode="w", index=False, header=True)

# driver = webdriver.Chrome(ChromeDriverManager().install())

# driver.get(TSDB.login)

# driver.find_element_by_name("username").send_keys(TSDB.username)
# driver.find_element_by_name("password").send_keys(TSDB.password)
# driver.find_element_by_xpath("/html/body/section/div/div[3]/div/form/div[4]/input").click()

# for line in df.itertuples():
#     driver.get(TSDB.add)
#     driver.find_element_by_name("datepicker").clear();
#     driver.find_element_by_name("datepicker").send_keys(line.date)
#     driver.find_element_by_name("season").send_keys(line.season)
#     driver.find_element_by_name("eventcountry").send_keys(line.country)
#     if pd.isna(line.location):
#         pass
#     else:
#         driver.find_element_by_name("eventcity").send_keys(line.location)
#     driver.find_element_by_name("eventname").send_keys(line.event)
#     driver.find_element_by_name("submit").click()
#     driver.implicitly_wait(5)

#     get_id = driver.find_element_by_link_text("Edit additional event details here").get_attribute('href');
#     driver.get(get_id)

#     driver.implicitly_wait(5)
#     if pd.isna(line.card):
#         pass
#     else:
#         driver.find_element_by_name("descriptionEN").send_keys(line.card)
#     if pd.isna(line.results):
#         pass
#     else:
#         driver.find_element_by_name("result").send_keys(line.results)
#     driver.find_element_by_name("submit").click()

# driver.quit()