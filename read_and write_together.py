import requests
import threading
import json
import time


start = time.time()
# Lock object to threads be safe
file_lock = threading.Lock()

# file to write retrieved data
filename = "retrieve_and_write_together.json"

def fetch_and_write_data(post_id):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(url)
    post_data = response.json()

    # write to the file
    with file_lock:
        with open(filename, "a") as s:
            json.dump(post_data, s)
            s.write(", \n")

# initialize file with 'w' flag to rewrite information and start with json bracket '['
with open(filename, 'w') as f:
    f.write('[\n')


threads = []
for i in range(1, 78):  # 1 to 77 inclusive
    t = threading.Thread(target=fetch_and_write_data, args=(i,))
    t.start()
    threads.append(t)



# Wait for all threads to finish
for t in threads:
    t.join()

# Write the closing JSON array bracket
with open(filename, 'a') as f:
    f.write(']\n')

end = time.time()
print(f"time spend for operation - {end - start}")

print("Done")