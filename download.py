from genericpath import isfile
import os
import shutil
import logging
import requests
import argparse
from utils import get_no_pages
from PIL import Image  # install by > python3 -m pip install --upgrade Pillow  # ref. https://pillow.readthedocs.io/en/latest/installation.html#basic-installation

BASE_URL = "http://web2.anl.az:81/read/img.php?"

logger = logging.getLogger('main')
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--id', required=True,
                    type=int, help='book ID')
parser.add_argument('--start-page', type=int, default=1,
                    help='starting page of the book')
parser.add_argument('--end-page', type=int, default=-1,
                    help='ending page of the book')
parser.add_argument('--pdf', action="store_true",
                    help='convert to PDF (or not)')

args = parser.parse_args()

bibid = args.id
start = args.start_page
ending = args.end_page if args.end_page != -1 else get_no_pages(bibid)
pdf = args.pdf

image_paths = []

for pno in range(start, ending+1):
    image_url = f"{BASE_URL}bibid={bibid}&pno={pno}"
    file_path = os.path.join("temp", str(bibid)+"_"+str(pno)+".jpeg")

#    if not os.path.isfile(file_path):
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        image_paths.append(file_path)
        with open(file_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        logging.info("failed to download image")

image_paths = list(os.walk("temp"))[0][2]
if pdf:
    images = [
        Image.open(image) for image in image_paths
        ]

    print(len(images))

    pdf_path = os.path.join("out", str(bibid)+".pdf")

    images[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )
