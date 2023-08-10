import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib.parse import urljoin
import os

def is_valid_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def show_and_save_images(url_list, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        img_tags = soup.find_all('img')
        if not img_tags:
            print(f"No images found on the webpage {url}.")
            continue

        base_url = response.url 

        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url:
                img_url = urljoin(base_url, img_url)  # Convert relative URL to absolute URL
                try:
                    img_response = requests.get(img_url)
                    img = Image.open(BytesIO(img_response.content))

                    # Check if the image is a .png file
                    if os.path.splitext(img_url)[1].lower() == ".png":
                        img_filename = os.path.splitext(os.path.basename(img_url))[0]
                        if is_valid_integer(img_filename):
                            img_path = os.path.join(save_folder, f"{img_filename}.png")
                            img.save(img_path)
                            print(f"Saved image {img_filename}.png")
                        else:
                            print("Skipping image:", img_filename, "(not an integer)")
                except Exception as e:
                    print(f"Error loading image: {e}")

if __name__ == "__main__":
    url_list = ["https://web.archive.org/web/20230415170154/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230416202932/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230417101322/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230420212008/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230422162325/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230423173309/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230425021414/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230426015725/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230427221704/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230428161242/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230430010748/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230502072116/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230510034110/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230531171802/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230605195037/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230608040246/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230324130419/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230318134540/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230316111748/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230320104741/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230309110511/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230310110002/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230303064549/http://www.setgame.com/set/puzzle",
                "https://web.archive.org/web/20230302050846/http://www.setgame.com/set/puzzle"
                ]  # Add more URLs to this list
    save_folder = "/Users/dimitrichrysafis/PycharmProjects/SetSolverRequests/images"
    show_and_save_images(url_list, save_folder)
