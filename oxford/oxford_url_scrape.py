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
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
    }
  )
  
  urls = []
  
  for page in range(4):
    doc = requests.get(f"https://podcasts.ox.ac.uk/series?combine=&page={page}", headers=headers)
    soup = BeautifulSoup(doc.text, "html.parser")
    
    rows = soup.find("div", class_="view-series-listing").find("div", class_="view-content").find_all("div", class_="views-row")

    for i, row in enumerate(rows):
      a_tag = row.find("div", class_="views-field-rendered-entity").find("a")
      lecture_url = extract_link(a_tag)
      
      # video를 가지고 있는 강의인지 판별
      lecture_doc = requests.get(lecture_url, headers=headers)
      lecture_soup = BeautifulSoup(lecture_doc.text, "html.parser")
    
      # is contain "Apple Podcast Video"?
      apple_podcast_video = lecture_soup.find("div", class_="subscriptions").find("a", class_="apple-podcast-video")
      if apple_podcast_video.get_text() == "Apple Podcast Video":
        urls.append(extract_link(a_tag))
      
      print(f"{page + 1}/4 {i + 1}/{len(rows)}")
      
  with open("./oxford/oxford_urls.json", 'w') as d:
    json.dump(urls, d)
  return
  
  # for row in rows:
  #   a_tag = row.find("div", class_="views-field-name").find("a")
  #   urls.append(extract_link(a_tag))
    
  # urls_having_video = []
  
  # for idx, url in enumerate(urls):
  #   doc_2 = requests.get(url, headers=headers)
  #   soup_2 = BeautifulSoup(doc_2.text, "html.parser")
    
  #   subscribe_row = soup_2.find(id="block-views-taxonomy_term_files-subscribe")
  #   a_tags = subscribe_row.find_all("a")
  #   strings = list(map(extract_string, a_tags))
    
  #   if search(strings, "Apple Podcasts Video") and search(strings, "Video RSS Feed"):
  #     urls_having_video.append(url)
      
  #   print(f"{idx} / {len(urls)}")
  
  # print(f"urls_having_video: {len(urls_having_video)}")
  