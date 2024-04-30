# PDF Text Extractor with OCR

## Overview
This project provides a Python-based tool for extracting text from PDF files, including handling text within images using Optical Character Recognition (OCR). It utilizes a combination of libraries like PyPDF2, pdfminer, pdfplumber, and pytesseract to handle various elements within PDF documents, such as text layers, images, and tables.

## Why Use OCR When I have Large Language Models?
Large language models (LLMs), such as GPT, often struggle with processing text directly from scanned PDFs. Scanned documents are essentially images of text, which can contain various distortions like noise, skewing, and inconsistent formatting. Using OCR (Optical Character Recognition) technology is a crucial step to bridge this gap. OCR systems are specifically designed to recognize text in images, handling a wide range of document quality and text styles. By converting scanned documents into clean, machine-readable text through OCR, we can significantly enhance the accuracy of subsequent analyses by LLMs.


## Features
- **Text Extraction**: Extracts plain text from PDF files using pdfminer.
- **Image Text Recognition**: Uses pytesseract to perform OCR on text embedded in images within the PDF.
- **Table Recognition**: Extracts and formats text from tables using pdfplumber.
- **Batch Processing**: Can process multiple PDFs in a specified folder.

## Prerequisites
To run this tool, you need Python 3.7 or later. You will also need to install several dependencies and have the Tesseract-OCR engine installed on your machine.

### Dependencies
- PyPDF2
- pdfminer.six
- pdfplumber
- PIL (Pillow)
- pytesseract
- OpenCV-python
- numpy

### Installation
To install Tesseract-OCR, follow the instructions specific to your operating system. You can find the instructions on the [Tesseract GitHub page](https://github.com/tesseract-ocr/tesseract).

### Python Libraries
Install the required Python libraries using pip:
```bash
pip install PyPDF2 pdfminer.six pdfplumber Pillow pytesseract opencv-python numpy
