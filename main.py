import time
import pickle
from mit.mit_lecture_scrape import get_lecture_info

start_time = time.time()

get_lecture_info()

end_time = time.time()
total_time = end_time - start_time
minutes = round(total_time // 60, 0)
seconds = round(total_time % 60, 2)

print(f"total time: {minutes}m {seconds}s")
