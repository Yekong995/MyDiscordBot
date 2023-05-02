"""
Lib for nsfw functions.
"""

import requests
import random
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
        img_data = requests.get(img, headers=self.user_agent)
        with open('image.jpg', 'wb') as handler:
            handler.write(img_data.content)
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
        img_data = requests.get(img, headers=self.user_agent)
        with open('image.jpg', 'wb') as handler:
            handler.write(img_data.content)
        return "image.jpg"
