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

def extract_src(soup_element):
  return urljoin(BASE_URL, soup_element.attrs['src'])

def get_lecture_video_info():
  lecture_urls = []
  with open('./oxford/oxford_urls.json') as json_file:
    lecture_urls = json.load(json_file)
  
  headers = requests.utils.default_headers()
  headers.update(
    {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
    }
  )

  lectures = []
  videos = []
  audio = 0
  
  for idx, lecture_url in enumerate(lecture_urls):
    lecture_doc = requests.get(lecture_url, headers=headers)
    lecture_soup = BeautifulSoup(lecture_doc.text, "html.parser")
    
    # do exist pagenation?
    page_nav = lecture_soup.find("nav", class_="layout--content-medium")
    if page_nav is not None:
      continue
    
    # Lecture Info
    lecture_idx = idx
    lecture_institute = "Oxford University"
    lecture_levels = ["Overall"]
    lecture_title = extract_text(lecture_soup.find("h1", class_="field--name-node-title"))
    lecture_thumbnail_url = extract_src(lecture_soup.find("div", class_="field--type-image").find("img"))
    
    series_content = lecture_soup.find("div", class_="series-content")
    lecture_description = extract_text(series_content.find("div", class_="text-content"))
    
    lecture_instructors = []
    lecture_topics = []
    lecture_as_taught_in = ""
    
    videos_of_lecture = []
    
    # Video Info
    table = lecture_soup.find("table", class_="views-table")
    trs = list(reversed(table.find("tbody").find_all("tr")))
    
    for i, tr in enumerate(trs):
      if i == 0:
        lecture_as_taught_in = extract_text(tr.find("td", class_="views-field-created"))[-4:]
      
      instructor_a_tags = tr.find("td", class_="views-field-field-contributor").find_all("a")
      for instructor_a_tag in instructor_a_tags:
        lecture_instructors.append(extract_text(instructor_a_tag))
        
      a_tag = tr.find("td", class_="views-field-title").find("a")
      video_url = extract_link(a_tag)
      video_title = extract_text(a_tag)
      video_description = extract_text(tr.find("td", class_="views-field-field-short-description"))
      video_player = "Oxford"
      
      # Enter the video link
      video_doc = requests.get(video_url, headers=headers)
      video_soup = BeautifulSoup(video_doc.text, "html.parser")
      
      topic_items = video_soup.find("div", class_="video-info-container").find("div", class_="field--name-field-keywords").find("div", class_="field__items").find_all("div", class_="field__item")
      for topic_item in topic_items:
        lecture_topics.append(extract_text(topic_item.find("a")))
      
      # Is have video?
      video_btn = video_soup.find("div", class_="article-header").find("div", class_="btn-wrapper").find("a")
      if extract_text(video_btn) != "Video":
        audio = audio + 1
        print(f"Audio: {audio}")
      
      # Is have both video and audio?
      video_btns = video_soup.find("div", class_="article-header").find("div", class_="btn-wrapper").find_all("a")
      if len(video_btns) > 2:
        print("Both Video Audio", video_url)
        
      video_link = video_soup.find("div", class_="downloads").find("div", class_="download-links").find("a")
      if video_link is None:
        continue
      video_src = video_link.attrs["href"]
      
      videos_of_lecture.append({
        "videoLink": video_url,
        "thumbnailUrl": lecture_thumbnail_url,
        "idx": idx,
        "title": video_title,
        "description": video_description,
        "player": video_player,
        "videoSrc": video_src,
      })
    
      print(f"{idx + 1}/{len(lecture_urls)} {i + 1}/{len(trs)}")
    
    videos.append(videos_of_lecture)
    lectures.append({
      "lectureIdx": lecture_idx,
      "title": lecture_title,
      "instructors": lecture_instructors,
      "topics": lecture_topics,
      "as_taught_in": lecture_as_taught_in,
      "institute": lecture_institute,
      "levels": lecture_levels,
      "thumbnailUrl": lecture_thumbnail_url,
      "description": lecture_description,
      "lectureLink": lecture_url,
    })
  
  with open("./oxford/oxford_lectures.json", 'w') as d:
    json.dump(lectures, d)
  with open("./oxford/oxford_videos.json", 'w') as d:
    json.dump(videos, d)