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

def print_card_info(x):
    def get_color(x):
        c = ((x - 1) // 3) % 3
        if c == 0:
            return "RED"
        elif c == 1:
            return "PURPLE"
        else:
            return "GREEN"

    def get_number(x):
        return ((x - 1) % 3) + 1

    def get_shape(x):
        d = ((x - 1) // 9) % 3
        if d == 0:
            return "SQUIGGLY"
        elif d == 1:
            return "DIAMOND"
        else:
            return "OVAL"

    def get_shade(x):
        f = ((x - 1) // 27) % 3
        if f == 0:
            return "FULLY"
        elif f == 1:
            return "PARTIAL"
        else:
            return "NONE"

    color = get_color(x)
    number = get_number(x)
    shape = get_shape(x)
    shade = get_shade(x)

    return "({},{},{},{},{})".format(x, color, number, shape, shade)

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

    # Check combinations of 3 from the array
    for combo in combinations(valid_image_filenames, 3):
        if form_set(combo[0], combo[1], combo[2]):
            print("Set found:", [print_card_info(x) for x in combo])

def form_set(x, y, z):
    for i in range(0, 4):
        s = set([((x - 1)//(3**i)) % 3, ((y - 1)//(3**i)) % 3, ((z - 1)//(3**i)) % 3])
        if len(s) % 2 == 0:
            return False
    return True

if __name__ == "__main__":
    website_url = "http://www.setgame.com/set/puzzle"  # Replace with the desired website URL
    show_png_images(website_url)
