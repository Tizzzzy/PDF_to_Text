import PyPDF2
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
import pdfplumber
from PIL import Image
from pdf2image import convert_from_path
import pytesseract 
import os
import cv2
import numpy as np
import argparse

from os import path
from glob import glob  

poppler_path = r'C:\Program Files\poppler-23.11.0\Library\bin'

def find_ext(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))

def text_extraction(element):
    line_text = element.get_text()
    

    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            for character in text_line:
                if isinstance(character, LTChar):
                    line_formats.append(character.fontname)
                    line_formats.append(character.size)
    format_per_line = list(set(line_formats))
    
    return (line_text, format_per_line)

def crop_image(element, pageObj):
    [image_left, image_top, image_right, image_bottom] = [element.x0,element.y0,element.x1,element.y1] 
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(pageObj)
    with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

def convert_to_images(input_file,):
    images = convert_from_path(input_file, poppler_path=poppler_path)
    image = images[0]
    output_file = "PDF_image.png"
    image.save(output_file, "PNG")

def image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text



def extract_table(pdf_path, page_num, table_num):
    pdf = pdfplumber.open(pdf_path)
    table_page = pdf.pages[page_num]
    table = table_page.extract_tables()[table_num]
    return table

def table_converter(table):
    table_string = ''
    for row_num in range(len(table)):
        row = table[row_num]
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        table_string+=('|'+'|'.join(cleaned_row)+'|'+'\n')
    table_string = table_string[:-1]
    return table_string

def main(folder_path, type="pdf"):
    paths = find_ext(folder_path, type)
    print(paths)

    for pdf_path in paths:
        pdfFileObj = open(pdf_path, 'rb')
        pdfReaded = PyPDF2.PdfReader(pdfFileObj)

        text_per_page = {}
        for pagenum, page in enumerate(extract_pages(pdf_path)):
            
            pageObj = pdfReaded.pages[pagenum]
            page_text = []
            line_format = []
            text_from_images = []
            text_from_tables = []
            page_content = []
            table_num = 0
            first_element= True
            table_extraction_flag= False
            pdf = pdfplumber.open(pdf_path)
            page_tables = pdf.pages[pagenum]
            tables = page_tables.find_tables()


            page_elements = [(element.y1, element) for element in page._objs]
            page_elements.sort(key=lambda a: a[0], reverse=True)

            lower_side = 0
            upper_side = 0

            for i,component in enumerate(page_elements):
                pos= component[0]
                element = component[1]
                
                if isinstance(element, LTTextContainer):
                    if table_extraction_flag == False:
                        (line_text, format_per_line) = text_extraction(element)
                        page_text.append(line_text)
                        line_format.append(format_per_line)
                        page_content.append(line_text)
                    else:
                        pass

                if isinstance(element, LTFigure):
                    crop_image(element, pageObj)
                    convert_to_images('cropped_image.pdf')
                    image_text = image_to_text('PDF_image.png')
                    text_from_images.append(image_text)
                    page_content.append(image_text)
                    page_text.append('image')
                    line_format.append('image')

                if isinstance(element, LTRect):
                    if first_element == True and (table_num+1) <= len(tables):
                        lower_side = page.bbox[3] - tables[table_num].bbox[3]
                        upper_side = element.y1 
                        table = extract_table(pdf_path, pagenum, table_num)
                        table_string = table_converter(table)
                        text_from_tables.append(table_string)
                        page_content.append(table_string)
                        table_extraction_flag = True
                        first_element = False
                        page_text.append('table')
                        line_format.append('table')

                    if element.y0 >= lower_side and element.y1 <= upper_side:
                        pass
                    elif (i+1) < len(page_elements) and not isinstance(page_elements[i+1][1], LTRect):
                        table_extraction_flag = False
                        first_element = True
                        table_num+=1
                    else:
                        table_extraction_flag = False
                        first_element = True


            dctkey = 'Page_'+str(pagenum)
            text_per_page[dctkey]= [page_text, line_format, text_from_images,text_from_tables, page_content]

        pdfFileObj.close()

        # Deleting the additional files created
        # os.remove('cropped_image.pdf')
        # os.remove('PDF_image.png')

        # Display the content of the page
        # result = ''.join(text_per_page['Page_0'][4])
        # print(result)

        file_name = pdf_path.split('.')[0]

        file_path = f"{file_name}.txt"

        with open(file_path, 'w', encoding='utf-8') as file:
            result = ''
            for page in range(len(text_per_page)):
                result += ''.join(text_per_page[f"Page_{page}"][4])
                
            file.write(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extracts text from PDF.")
    parser.add_argument("-folder_path", required=True, help="Path to the folder containing PDF files")
    args = parser.parse_args()
    
    main(args.folder_path)