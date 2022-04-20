import json
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "http://podcasts.ox.ac.uk"

def extract_link(a_tag):
  return urljoin(BASE_URL, a_tag.attrs['href'])

def extract_string(soup_element):
  return soup_element.string.strip()

def search(list, str):
  for i in range(len(list)):
    if list[i] == str:
        return True
  return False


def get_urls():
  headers = requests.utils.default_headers()
  headers.update(
    {
      'User-Agent': 'My User Agent 1.0',
    }
  )
  
  doc = requests.get("http://podcasts.ox.ac.uk/open/all?sort_by=created&sort_order=DESC&items_per_page=All", headers=headers)
  soup = BeautifulSoup(doc.text, "html.parser")
  
  rows = soup.find_all("li", class_="views-row")
  
  urls = []
  
  for row in rows:
    a_tag = row.find("div", class_="views-field-name").find("a")
    urls.append(extract_link(a_tag))
    
  urls_having_video = []
  
  for idx, url in enumerate(urls):
    doc_2 = requests.get(url, headers=headers)
    soup_2 = BeautifulSoup(doc_2.text, "html.parser")
    
    subscribe_row = soup_2.find(id="block-views-taxonomy_term_files-subscribe")
    a_tags = subscribe_row.find_all("a")
    strings = list(map(extract_string, a_tags))
    
    if search(strings, "Apple Podcasts Video") and search(strings, "Video RSS Feed"):
      urls_having_video.append(url)
      
    print(f"{idx} / {len(urls)}")
  
  print(f"urls_having_video: {len(urls_having_video)}")
  
  with open("./oxford/oxford_urls.json", 'w') as d:
    json.dump(urls_having_video, d)
  return