import threading
import requests
import queue
import json
import time




class FetchingPosts:
    def __init__(self, file_name, num_posts, url_for_retrieve):
        self.url_for_retrieve = url_for_retrieve
        self.file_name = file_name
        self.num_posts = num_posts
        self.post_queue = queue.Queue()
        self.file_lock = threading.Lock()

    # Function to fetch post and add it in Queue
    def fetch_post(self, post_id):
        url = self.url_for_retrieve + str(post_id)
        response = requests.get(url)
        post_data = response.json()
        self.post_queue.put(post_data)

    # save posts from queue to file
    def save_post_to_file(self):
        with open(self.file_name, 'w') as f:
            while True:
                post_data = self.post_queue.get()
                if post_data is None:
                    break
                with self.file_lock:
                    json.dump(post_data, f)
                    f.write(', \n')
                    self.post_queue.task_done()


    # run fetching and writing process
    def run_fetching_and_writing(self):
        start = time.time()
        with open(self.file_name, 'w') as f:       # 'w' means overwrite if data is already in file
            f.write(' [ \n')


        # threads to fetch data
        threads = []
        for i in range(1, self.num_posts + 1):
            t = threading.Thread(target=self.fetch_post, args=( i,))
            t.start()
            threads.append(t)

        # start thread to save the posts in file
        save_thread = threading.Thread(target=self.save_post_to_file)
        save_thread.start()


        # wait for all threads to finish
        for t in threads:
            t.join()

        # add none at the end of queue
        self.post_queue.put(None)


        # wait for save thread
        save_thread.join()


        # closing json array bracket
        with open(self.file_name, 'a') as f:
            f.write('] \n')


        end = time.time()
        print(f"time spend for operation: {end - start}")


if __name__ == '__main__':
    fetcher = FetchingPosts(file_name='posts.json', num_posts=77, url_for_retrieve='https://jsonplaceholder.typicode.com/posts/')
    fetcher.run_fetching_and_writing()


