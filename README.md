# Book Retriever for Azerbaijan National Library
This CLI tool is used to download books from Azerbaijan National Library.

# HOWTO
## Ubuntu
Clone the project:
```
git clone https://github.com/ceferisbarov/anl-retrieval-cli
```

Install the requirements:
```
cd anl-retrieval-cli
pip3 install -r requirements
```
Install the book (id=999999), convert to PDF and perform OCR:
```
python download.py -id 999999 --pdf --ocr
```

You can also specify the page interval to download:
```bash
python download.py --id 999999 --start-page 18 --end-page 59 --pdf --ocr 
```

## Windows
Not yet available.

## MacOS
Not yet available.

# Progress and contribution

For further inquiries, contact me: cefer.isbarov@gmail.com