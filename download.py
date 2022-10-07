import os
import shutil
import logging
import requests
import argparse
from utils import get_no_pages, is_jpg
from PIL import Image
import ocrmypdf

BASE_IMAGE_URL = "http://web2.anl.az:81/read/img.php?"
BASE_PAGE_URL = "http://web2.anl.az:81/read/page.php?"
IMAGE_EXTENSIONS = ("jpeg", "JPEG", "jpg", "JPG", "png", "PNG")

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
parser.add_argument('--ocr', action="store_true",
                    help='OCR the pdf (or not)')

args = parser.parse_args()
bibid = args.id
start = args.start_page
ending = args.end_page if args.end_page != -1 else get_no_pages(bibid)
pdf = args.pdf
ocr = args.ocr
if ocr and not pdf:
    logger.warning("You have opted to not create a PDF, but use OCR. This is not possible.\
                    OCR choice is going to be ignored.")

for pno in range(start, ending+1):
    image_url = f"{BASE_IMAGE_URL}bibid={bibid}&pno={pno}"
    jpg_path = os.path.join("temp", str(bibid)+"_"+str(pno)+".jpeg")
    png_path = os.path.join("temp", str(bibid)+"_"+str(pno)+".png")
    
    if not os.path.isfile(jpg_path) and not os.path.isfile(png_path):
        page_url = f"{BASE_PAGE_URL}bibid={bibid}&pno={pno}"
        _ = requests.get(page_url)
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            with open(jpg_path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

            if not is_jpg(jpg_path):
                os.remove(jpg_path)
                with open(png_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            
        
            logger.info(f"download page no. {pno}")

    else:
        logger.info(f"failed to download page no. {pno}")

temp_files = list(os.walk("temp"))[0][2]
image_files = [file_path for file_path in temp_files if file_path.endswith(IMAGE_EXTENSIONS)]
image_paths = [os.path.join("temp", image_file) for image_file in image_files]
sorted_image_paths = sorted(image_paths, key=lambda x: int(x.split("_")[-1].split(".")[0]))

if pdf:
    pdf_path = os.path.join("out", str(bibid)+".pdf")
    if not os.path.isfile(pdf_path):
        images = [
            Image.open(image) for image in sorted_image_paths
            ]


        images[0].save(
            pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
        )

        logger.info("converted to PDF")

    else:
        logger.info("PDF already exists")

if pdf and ocr:
    save_path = os.path.join("out", str(bibid)+"_ocr.pdf")
    if os.path.isfile(save_path):
        logger.warning("OCR file already exists. Skipping OCR.")

    else:
        ocrmypdf.ocr(pdf_path, save_path, rotate_pages=True,
                            remove_background=False, language="aze",
                            deskew=True, force_ocr=True)  # TODO: Add language options
        logger.info("OCR performed")