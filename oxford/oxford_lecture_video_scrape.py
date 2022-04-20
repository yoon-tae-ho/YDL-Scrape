import json
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "http://podcasts.ox.ac.uk"

def search(list, str):
  for i in range(len(list)):
    if list[i] == str:
        return True
  return False

def extract_text(soup_element):
  return soup_element.get_text().strip()

def extract_string(soup_element):
  return soup_element.string.strip()

def extract_link(a_tag):
  return urljoin(BASE_URL, a_tag.attrs['href'])

def get_lecture_video_info():
  lecture_urls = []
  with open('./oxford/oxford_urls.json') as json_file:
    lecture_urls = json.load(json_file)
  
  headers = requests.utils.default_headers()
  headers.update(
    {
      'User-Agent': 'My User Agent 1.0',
    }
  )

  lectures = []
  videos = []

  for idx, lecture_url in enumerate(lecture_urls):
    # lecture info
    lecture_doc = requests.get(lecture_url, headers=headers)
    lecture_soup = BeautifulSoup(lecture_doc.text, "html.parser")
    
    lecture_idx = idx
    lecture_title = extract_string(lecture_soup.find(id="content-header").find("h1", class_="title"))
    lecture_description = extract_text(lecture_soup.find("div", class_="views-field-description").find("div", class_="field-content"))
    lecture_thumbnail_url = lecture_soup.find(id="content-area").find("img").attrs["src"]
    
    rows = lecture_soup.find("table", class_="views-table").find("tbody").find_all("tr")
    rows.reverse()
    
    lecture_as_taught_in = extract_string(rows[0].find("td", class_="views-field-created"))[-4:]
    
    lecture_topics = []
    lecture_instructors = []
    videos_in_a_lecture = []
    for row_idx, row in enumerate(rows):
    # get instructors
      names = list(map(extract_string, row.find("td", class_="views-field-field-people").find_all("a")))
      for name in names:
        if not search(lecture_instructors, name):
          lecture_instructors.append(name)
          
      # video info
      video_url = extract_link(row.find("td", class_="views-field-title").find("a"))
      video_doc = requests.get(video_url, headers=headers)
      video_soup = BeautifulSoup(video_doc.text, "html.parser")

      video_idx = idx
      video_thumbnail_url = lecture_thumbnail_url
      is_video = video_soup.find(id="quicktabs-tab-media_player-0")
      video_type = "Audio" if is_video == None else "Video"
      
      video_title = extract_string(video_soup.find(id="content-header").find("h1", class_="title"))

      content_area = video_soup.find(id="content-area")
      video_description = extract_text(content_area.find("div", class_="views-field-body").find("div", class_="field-content"))
      video_embeded_code = content_area.find(id="block-views-embed_codes-block").find("a", class_="ox-jwplayer-embed-link").attrs["href"][31:]

      videos_in_a_lecture.append({
        "videoLink": video_url,
        "thumbnailUrl": video_thumbnail_url,
        "idx": video_idx,
        "title": video_title,
        "embededCode": video_embeded_code,
        "description": video_description,
        "player": "Oxford",
        "type": video_type
      })
      
      # get lecture topics
      video_topics = list(map(extract_string, content_area.find("div", class_="views-field-field-keywords").find_all("a")))
      for video_topic in video_topics:
        if not search(lecture_topics, video_topic):
          lecture_topics.append(video_topic)
          
      print(f"lecture_idx: {idx}/{len(lecture_urls)}, video_idx: {row_idx}/{len(rows)}")
          
    lectures.append({
      "lectureIdx": lecture_idx,
      "title": lecture_title,
      "instructors": lecture_instructors,
      "topics": lecture_topics,
      "asTaughtIn": lecture_as_taught_in,
      "institute": "Oxford University",
      "levels": [],
      "description": lecture_description,
      "thumbnailUrl": lecture_thumbnail_url,
      "lectureLink": lecture_url,
    })
    videos.append(videos_in_a_lecture)


  with open("./oxford/oxford_lectures.json", 'w') as d:
    json.dump(lectures, d)
  with open("./oxford/oxford_videos.json", 'w') as d:
    json.dump(videos, d)
    
    
  # video: id="quicktabs-tab-media_player-0"
  # audio: id="quicktabs-tab-media_player-1"