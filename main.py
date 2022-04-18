import time
import pickle
from mit.mit_lecture_scrape import get_lecture_info
from mit.mit_video_scrape import get_video_info
from mit.check_nav_types import check_nav_types

start_time = time.time()

# get_lecture_info()
get_video_info()
# check_nav_types()

end_time = time.time()
total_time = end_time - start_time
minutes = round(total_time // 60, 0)
seconds = round(total_time % 60, 2)

print(f"total time: {minutes}m {seconds}s")
