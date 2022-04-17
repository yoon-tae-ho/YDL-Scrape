import pickle
import time
from mit.mit_url_scrape import get_urls as get_mit_urls

start_time = time.time()

get_mit_urls()

end_time = time.time()
total_time = end_time - start_time
minutes = round(total_time // 60, 0)
seconds = round(total_time % 60, 2)

print(f"total time: {minutes}m {seconds}s")

# inp = open('mit_urls', 'rb')
# cust = pickle.load(inp)
# print(cust[0])
# inp.close()
