import enum
import json
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://oyc.yale.edu"

def extract_link(a_tag):
  return urljoin(BASE_URL, a_tag.attrs['href'])

def extract_string(soup_element):
  return soup_element.get_text().strip()

def search(list, str):
  for i in range(len(list)):
    if list[i] == str:
        return True
  return False

def get_lecture_preview():
  headers = requests.utils.default_headers()
  headers.update(
    {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
    }
  )
  
  doc = requests.get(BASE_URL + "/courses", headers=headers)
  soup = BeautifulSoup(doc.text, "html.parser")
  
  rows = soup.find(id="block-system-main").find("table", class_="views-table").find("tbody").find_all("tr")
  
  lectures = []
  
  for i, row in enumerate(rows):
    department = extract_string(row.find("td", class_="views-field-title").find("a"))
    title = extract_string(row.find("td", class_="views-field-title-1").find("a"))
    instructors = [extract_string(row.find("td", class_="views-field-field-professors-last-name"))]
    as_taught_in = extract_string(row.find("td", class_="views-field-field-semester"))[-4:]
    institute = "Yale University"
    levels = ["overall"]
    
    # department로부터 topics 만들기
    topics = department.split(' ')
    
    # ,를 처리
    if i == 27:
      topics[0] = topics[0][0:-1]
    
    # and, of 처리
    for str in topics:
      if str == "and":
        topics.remove("and")
      elif str == "of":
        topics.remove("of")
    
    if len(topics) > 1:
      topics.append(department)

    lectures.append({
      "lectureIdx": i,
      "title": title,
      "instructors": instructors,
      "topics": topics,
      "as_taught_in": as_taught_in,
      "institute": institute,
      "levels": levels,
    })
    
  return lectures
  
def get_lecture_info():
  lectures = get_lecture_preview()

  # yale_urls.json으로부터 lecture url 읽어오기
  urls = []
  with open('./yale/yale_urls.json') as json_file:
    urls = json.load(json_file)
  
  for idx, url in enumerate(urls):
    headers = requests.utils.default_headers()
    headers.update(
      {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
      }
    )

    doc = requests.get(url, headers=headers)
    soup = BeautifulSoup(doc.text, "html.parser")
    
    thumbnail_url = urljoin(BASE_URL, soup.find("div", class_="views-field-field-course-header-image").find("img").attrs['src'])
    description = extract_string(soup.find(id="quicktabs-tabpage-course-0").find("div", class_="views-field-body").find("p"))
    
    lectures[idx]["thumbnailUrl"] = thumbnail_url
    lectures[idx]["description"] = description
    lectures[idx]["lectureLink"] = url
  
    print(idx)
  
  with open("./yale/yale_lectures.json", 'w') as d:
    json.dump(lectures, d)
  return
  
