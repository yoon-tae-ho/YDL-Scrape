import pickle
import json
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://ocw.mit.edu"

def extract_string(soup_element):
  return soup_element.string.strip()

def get_lecture_info():
  inp = open('./mit/mit_urls', 'rb')
  urls = pickle.load(inp)
  inp.close()
  
  lectures = []
  
  for idx, url in enumerate(urls):
    doc = requests.get(url)
    soup = BeautifulSoup(doc.text, "html.parser")
    
    title = soup.find(id="course-banner").find('a').string
    description = soup.find(id="course-description").string
    
    link = soup.find("img", class_="course-image").attrs['src']
    thumbnail_url = urljoin(BASE_URL, link)

    instructors = list(map(extract_string, soup.find_all("a", class_="course-info-instructor")))
    instructors = list(dict.fromkeys(instructors))  # process duplication
    topics = list(map(extract_string, soup.find_all("a", class_="course-info-topic")))
    topics = list(dict.fromkeys(topics))  # process duplication
    levels = list(map(extract_string, soup.find_all("a", class_="course-info-level")))
    levels = list(dict.fromkeys(levels))  # process duplication
    as_taught_in = url[-5:-1]
    institute = "Massachusetts Institute of Technology"
    
    lectures.append({
      "lectureIdx": idx,
      "title": title,
      "instructors": instructors,
      "topics": topics,
      "asTaughtIn": as_taught_in,
      "institute": institute,
      "levels": levels,
      "description": description,
      "thumbnailUrl": thumbnail_url,
    })
    print(idx)
    
  with open("./mit/mit_lectures.json", 'w') as d:
    json.dump(lectures, d)

