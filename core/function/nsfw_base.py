"""
Lib for nsfw functions.
"""

import requests
import random
from tqdm import tqdm
from bs4 import BeautifulSoup

class Rule34():

    def __init__(self) -> None:
        super(Rule34, self).__init__()
        self.random_url = "https://rule34.xxx/index.php?page=post&s=view&id="
        self.search_url = "https://rule34.xxx/index.php?page=post&s=list&tags="
        self.maxpage = 1000
        self.maxnum = 7899999

        self.user_agent = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def random_image(self) -> str:
        """
        Returns random image from rule34.xxx
        """
        num = random.randint(1, self.maxnum)
        url = self.random_url + str(num)
        r = requests.get(url, headers=self.user_agent)
        soup = BeautifulSoup(r.text, "lxml")
        img = soup.find("img", {"id": "image"})["src"]
        img_data = requests.get(img, headers=self.user_agent, stream=True)
        total_size_in_bytes= int(img_data.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc="Downloading image",
                            ascii=True, colour="magenta")
        with open('image.jpg', 'wb') as handler:
            for data in img_data.iter_content(block_size):
                progress_bar.update(len(data))
                handler.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")
        return "image.jpg"
    
    def search_img(self, title: str) -> str:
        """
        Returns random image from rule34.xxx
        """
        title = title.replace(" ", "_").lower()
        url = self.search_url + title + "&pid=" + str(random.randint(0, self.maxpage))
        r = requests.get(url, headers=self.user_agent)
        soup = BeautifulSoup(r.text, "lxml")
        span = soup.find_all("span", {"class": "thumb"})
        id = random.choice(span)['id'].replace("s", "")
        return id
    
    def get_img_by_id(self, id: str) -> str:
        """
        Returns image from rule34.xxx by id
        """
        url = self.random_url + id
        r = requests.get(url, headers=self.user_agent)
        soup = BeautifulSoup(r.text, "lxml")
        img = soup.find("img", {"id": "image"})["src"]
        img_data = requests.get(img, headers=self.user_agent, stream=True)
        total_size_in_bytes= int(img_data.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc="Downloading image",
                            ascii=True, colour="magenta")
        with open('image.jpg', 'wb') as handler:
            for data in img_data.iter_content(block_size):
                progress_bar.update(len(data))
                handler.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")
        return "image.jpg"
