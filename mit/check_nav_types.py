import pickle
import requests
import json
from bs4 import BeautifulSoup

def search(list, str):
  for i in range(len(list)):
    if list[i] == str:
        return True
  return False

def check_nav_types():
  inp = open('./mit/mit_urls', 'rb')
  urls = pickle.load(inp)
  inp.close()
  
  video_exist_num = 0
  video_str_types = []
  video_str_ex = []
  no_videos = []
  too_many_videos = []
  
  for idx, url in enumerate(urls):
    doc = requests.get(url)
    soup = BeautifulSoup(doc.text, "html.parser")
    
    # get a_tags of side nav
    course_nav = soup.find(id="course-nav")
    a_tags = course_nav.find_all("a")
    
    is_video_exist = False
    for i, a_tag in enumerate(a_tags):
      if a_tag.string == None:
        # print(f"idx: {idx}")
        # print(f"i: {i}")
        # print(f"url: {url}")
        # print("----")
        continue
      
      inner_text = a_tag.string.strip()
      if inner_text.lower().find("video") != -1:
        # video exist
        if is_video_exist:
          too_many_videos.append({
            "url": url,
            "idx": idx
          })
        else:
          is_video_exist = True
        
        if not search(video_str_types, inner_text):
          video_str_types.append(inner_text)
          video_str_ex.append({"url": url})
    
    if not is_video_exist:
      no_videos.append({
            "url": url,
            "idx": idx
      })
    else:
      ++video_exist_num
  
  print(f"video_exist_num: {video_exist_num}")
  print("-----------------------------------------------------")
  print("video_str_types: ")
  print(json.dumps(video_str_types, indent=2, sort_keys=True))
  print(len(video_str_types))
  print("-----------------------------------------------------")
  print("video_str_ex: ")
  print(json.dumps(video_str_ex, indent=2, sort_keys=True))
  print(len(video_str_ex))
  print("-----------------------------------------------------")
  print("no_videos: ")
  print(json.dumps(no_videos, indent=2, sort_keys=True))
  print(len(no_videos))
  print("-----------------------------------------------------")
  print("too_many_videos: ")
  print(json.dumps(too_many_videos, indent=2, sort_keys=True))
  print(len(too_many_videos))
  
