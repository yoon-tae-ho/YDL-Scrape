import enum
import time
import json
from oxford.oxford_url_scrape import get_urls
from oxford.oxford_lecture_video_scrape import get_lecture_video_info
# from yale.yale_urls_scrape import get_urls
# from yale.yale_lecture_scrape import get_lecture_info
# from yale.yale_video_scrape import get_video_info

start_time = time.time()

# get_urls()
get_lecture_video_info()

end_time = time.time()
total_time = end_time - start_time
minutes = round(total_time // 60, 0)
seconds = round(total_time % 60, 2)

print(f"total time: {minutes}m {seconds}s")
