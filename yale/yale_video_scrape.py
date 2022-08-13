from copyreg import constructor
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

def get_video_pages():
  # yale_urls.json으로부터 lecture url 읽어오기
  urls = []
  with open('./yale/yale_urls.json') as json_file:
    urls = json.load(json_file)
    
  videos = []
    
  for idx, url in enumerate(urls):
    headers = requests.utils.default_headers()
    headers.update(
      {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
      }
    )

    doc = requests.get(url, headers=headers)
    soup = BeautifulSoup(doc.text, "html.parser")
    
    session_tab = soup.find(id="quicktabs-tabpage-course-2")
    rows = session_tab.find("table", class_="views-table").find("tbody").find_all("tr")
    
    video_dicts = []
    
    for row in rows:
      session_num = extract_string(row.find("td", class_="views-field-field-session-display-number"))
      id = session_num.split(' ')[0]
      condition = id == "Lecture" or id == "Update" or id == "Lab" or id == "Paper"
      # "Paper Topics" "Lecture #" "Lab" "Update #"
      if condition:
        a_tag = row.find("td", class_="views-field-field-session-display-title").find("a")
        link = extract_link(a_tag)
        title = extract_string(a_tag)
        video_dicts.append({
          "videoLink": link,
          "title": title,
        })
        
    videos.append(video_dicts)
    print(idx)
    
  return videos

def get_video_info():
  video_pages = get_video_pages()
  
  videos = []
  
  for i, video_dicts in enumerate(video_pages):
    new_video_dicts = []
    for j, video_dict in enumerate(video_dicts):
      headers = requests.utils.default_headers()
      headers.update(
        {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
        }
      )

      doc = requests.get(video_dict["videoLink"], headers=headers)
      soup = BeautifulSoup(doc.text, "html.parser")
      
      video_block = soup.find("div", class_="block-session-video-player-block")
      if video_block is None:
        continue
      
      video_element = video_block.find("div", class_="view-session-video-player").find("div", class_="view-footer").find("video")
      
      thumbnail_url = video_element.attrs["poster"]
      idx = i
      description = extract_string(soup.find("div", class_="node-session").find("p"))
      player = "Yale"
      
      video_source_el = video_element.find("source")
      video_src = video_source_el.attrs["src"]
      video_type = video_source_el.attrs["type"]
      
      video_track_el = video_element.find("track")
      track_src = video_track_el.attrs["src"]
      track_kind = video_track_el.attrs["kind"]
      track_srclang = video_track_el.attrs["srclang"]
      
      new_video_dicts.append({
        "videoLink": video_dict["videoLink"],
        "thumbnailUrl": thumbnail_url,
        "idx": idx,
        "title": video_dict["title"],
        "description": description,
        "player": player,
        "videoSrc": video_src,
        "videoType": video_type,
        "trackSrc": track_src,
        "trackKind": track_kind,
        "trackSrclang": track_srclang,
      })
      print(f"{i + 1}/{len(video_pages)} {j + 1}/{len(video_dicts)}")
      
    videos.append(new_video_dicts)
    
  with open("./yale/yale_videos.json", 'w') as d:
    json.dump(videos, d)
  
    
# videoLink     X
# thumbnailUrl  X
# idx           X
# title         X
# embededCode
# description   X
# player        X
