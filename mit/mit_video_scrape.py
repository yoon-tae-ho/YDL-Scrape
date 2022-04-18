import pickle
import json
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://ocw.mit.edu"

case_1 = ["video lectures", "lecture videos", "video discussions", "lecture videos and slides", "class videos", "videos", "kanji video lectures", "concert videos", "lecture videos and notes", "lectures: video and slides", "lecture notes and video", "seminar videos", "videos for advanced lectures"]
case_pass = ["video and audio classes", "lecture notes and videos", "workshop videos", "lecture and lab videos", "video sessions", "calendar and videos", "video lectures and slides", "lecture videos and readings", "Video Lecture", "Lecture & Recitation Videos", "Class Session Videos", "Selected Videos", "Video Series Overview", "Session Video and Slides", "video"]

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

def get_video_dict(video_dict, idx):
  doc = requests.get(video_dict["videoLink"])
  soup = BeautifulSoup(doc.text, "html.parser")
  
  title = extract_string(soup.find(id="course-banner").find("a"))
  
  main_contents = soup.find(id="main-content")
  
  # get description
  text_box = main_contents.find(id="course-content-section")
  description_tag = text_box.find("p")
  description = ""
  if description_tag != None:
    description = extract_text(description_tag)[13:]
  
  video = main_contents.find("video", class_="video-js")
  embeded_code = json.loads(video.attrs["data-setup"])["sources"][0]["src"][30:]

  video_dict.update({
    "idx": idx,
    "title": title,
    "embededCode": embeded_code,
    "description": description,
    "player": "YouTube"
  })
  return video_dict

def get_video_pages(a_tag):
  doc = requests.get(extract_link(a_tag))
  soup = BeautifulSoup(doc.text, "html.parser")
  
  main_contents = soup.find(id="course-content-section")
  lecture_boxes = main_contents.find_all("div", class_="video-gallery-card")
  
  result = []
  for lecture_box in lecture_boxes:
    video_page = extract_link(lecture_box.find("a", class_="video-link"))
    thumbnail_url = lecture_box.find("img", class_="thumbnail").attrs["src"]
    result.append({
      "videoLink": video_page,
      "thumbnailUrl": thumbnail_url
    })
    
  return result

def get_video_info():
  inp = open('./mit/mit_urls', 'rb')
  urls = pickle.load(inp)
  inp.close()
  
  videos = []
  

  for idx, url in enumerate(urls):
    doc = requests.get(url)
    soup = BeautifulSoup(doc.text, "html.parser")
    
    # get a_tags of side nav
    course_nav = soup.find(id="course-nav")
    a_tags = course_nav.find_all("a")
    
    # get page links
    videos_of_lecture = []
    for a_tag in a_tags:
      if a_tag.string == None:
        break
      
      target = a_tag.string.strip().lower()
      
      if search(case_1, target) or url == "https://ocw.mit.edu/courses/21l-432-understanding-television-spring-2003/": # 후자는 예외
        videos_of_lecture.extend(get_video_pages(a_tag))
      # elif search(case_pass, target):
      #   continue
      else:
        continue
        
    if len(videos_of_lecture) != 0:
      for i, video_dict in enumerate(videos_of_lecture):
        videos_of_lecture[i] = get_video_dict(video_dict, idx)
    
    videos.append(videos_of_lecture)
    print(idx)
    
  with open("./mit/mit_videos.json", 'w') as d:
    json.dump(videos, d)
