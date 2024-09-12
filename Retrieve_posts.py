import threading
import requests
import json
import queue
import time


# Create a queue and lock object for thread-safe file writing
post_queue = queue.Queue()
file_lock = threading.Lock()

# The file where the posts will be saved
filename = 'retrieved_posts.json'

# Function to retrieve a post and put it in queue
def fetch_posts(post_id):
    url = f'https://jsonplaceholder.typicode.com/posts/{post_id}'
    response = requests.get(url)
    post_date = response.json()
    post_queue.put(post_date)


# Function to save posts to the file from the queue
def save_posts_to_file():
    with open(filename, 'a') as f: # 'a' flag is important to append new data in file and not altering existing data
        while True:
            post_data = post_queue.get()
            if post_data is None:
                break
            with file_lock:
                json.dump(post_data, f)
                f.write(', \n')
            post_queue.task_done()


start = time.time()
# initialize file, overwriting if it already exists, and write an opening JSON array bracket
with open(filename, 'w') as f:
    f.write('[ \n')


# Create and start threads to fetch the post
threads = []

for i in range(1, 78):
    t = threading.Thread(target=fetch_posts, args=(i,))
    t.start()
    threads.append(t)

# Start a thread to save the posts to the file
saver_thread = threading.Thread(target=save_posts_to_file)
saver_thread.start()

# Wait for all fetching threads to finish
for i in threads:
    i.join()


# Put None in Queue to indicate that fetching is completed
post_queue.put(None)

# Wait for the saver thread to finish
saver_thread.join()


# Write the closing JSON array bracket
with open(filename, 'a') as f:
    f.write('] \n')
end = time.time()
print(f"time spend for operation: {end - start}")
print('Done')




