import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from itertools import combinations

def is_valid_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def show_png_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    img_tags = soup.find_all('img')
    if not img_tags:
        print("no images found")
        return

    base_url = response.url
    valid_image_filenames = []

    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url:
            img_url = urljoin(base_url, img_url)
            try:
                img_filename = os.path.splitext(os.path.basename(img_url))[0]
                if os.path.splitext(img_url)[1].lower() == ".png" and is_valid_integer(img_filename):
                    valid_image_filenames.append(int(img_filename))
            except Exception as e:
                print(f"Error processing image: {e}")

    if valid_image_filenames:
        print("names")
        print(valid_image_filenames)
    else:
        print("n/a images.")
      
    for combo in combinations(valid_image_filenames, 3):
        if form_set(combo[0],combo[1],combo[2]):
            print("Set found:", combo)

def form_set (x, y, z) :
	for i in range(1, 4) :
		s = set([((x - 1)//(3**i)) % 3, ((y - 1)//(3**i)) % 3, ((z - 1)//(3**i)) % 3])
		if len(s) % 2 == 0 :
			return False
	return True

if __name__ == "__main__":
    website_url = "http://www.setgame.com/set/puzzle"  
    show_png_images(website_url)
