import json
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://oyc.yale.edu"

def extract_link(a_tag):
  return urljoin(BASE_URL, a_tag.attrs['href'])

def extract_string(soup_element):
  return soup_element.get_text()

def search(list, str):
  for i in range(len(list)):
    if list[i] == str:
        return True
  return False

def get_urls():
  headers = requests.utils.default_headers()
  headers.update(
    {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
    }
  )
  
  doc = requests.get(BASE_URL + "/courses", headers=headers)
  soup = BeautifulSoup(doc.text, "html.parser")
  
  rows = soup.find(id="block-system-main").find("table", class_="views-table").find("tbody").find_all("tr")
  
  yale_urls = []
  
  for row in rows:
    yale_urls.append(extract_link(row.find("td", class_="views-field-title-1").find("a")))
    
  # print(len(yale_urls))
  
  with open("./yale/yale_urls.json", 'w') as d:
    json.dump(yale_urls, d)
  return
