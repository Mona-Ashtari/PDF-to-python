import os
import pandas as pd
import PyPDF2
from io import BytesIO, StringIO
from PIL import Image
import fitz
import glob


def image_extractor(PDF_doc, page):
    image_list = page.get_images()
    images = []

    for image_index, img in enumerate(image_list):
        # get the XREF of the image
        xref = img[0]
        base_image = PDF_doc.extract_image(xref)
        image = Image.open(BytesIO(base_image['image']))
        images.append(image)
    return images


def text_extractor(page):
    page_text = page.get_text()
    if not len(page_text) == 0:
        string_text = StringIO(page_text)
        return string_text


def PDF_reader(data_path, PDF_name):

    # Creating a directory for the PDF
    if not os.path.exists(data_path + '\\' + PDF_name[:-4]):
        os.mkdir(data_path + '\\' + PDF_name[:-4])

    # Opening the PDF document
    PDF_doc = fitz.open(f'{data_path}\\{PDF_name}')

    # Iterating through pages of the PDF
    for page_index, page in enumerate(PDF_doc):

        # Extracting text from a PDF page
        string_text = text_extractor(page)

        # Saving text to CSV file
        if string_text:
            df = pd.read_csv(string_text, sep="\n")
            df.to_csv(f'{data_path}\\{PDF_name[:-4]}\\text_page{page_index}.csv', index=False)

        # Extracting images from page
        images_list = image_extractor(PDF_doc, page)

        # Saving images
        for i, im in enumerate(images_list):
            im.save(f'{data_path}\\{PDF_name[:-4]}\\page{page_index}_image{i}.png')


def main():
    data_path = r'' # Add the path to your data here
    PDF_names = [pdfname for pdfname in os.listdir(data_path) if pdfname.endswith('.pdf')]

    for PDF_name in PDF_names:
        PDF_reader(data_path, PDF_name)


if __name__ == '__main__':
    main()
