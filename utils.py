import requests
from PIL import Image

BASE_URL = "http://web2.anl.az:81/read/page.php?zoom=0&"

def get_no_pages(book_id):
    page_url = f"{BASE_URL}bibid={book_id}&pno=1"
    res = requests.get(page_url)
    for line in res.text.split("\n"):
        if "last_page_params" in line:
            idx = line.find("pno=")
            page_count = line[idx+4:].strip("\";")

            return int(page_count)

def is_jpg(file_path):
    try:
        Image.open(file_path)
    except:
        print(f"{file_path} not a jpeg!")
        return False
    return True
