from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from PyPDF2 import PdfReader, PdfWriter
import os

def add_pdf_watermark(input_pdf_path, output_pdf_path, watermark_pdf_path):
    pdf_reader = PdfReader('nwu-licence.pdf')
    pdf_writer = PdfWriter()
    
    # Load the watermark PDF
    watermark_reader = PdfReader(watermark_pdf_path)

    # Merge watermark into each page of the input PDF
    for page in pdf_reader.pages:
        page.merge_page(watermark_reader.pages[0])  # Assuming watermark is a single page
        pdf_writer.add_page(page)

    with open(output_pdf_path, 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)

def add_watermark(input_image_path, output_image_path, watermark_text):
    try:
        original = Image.open('nwu-licence.png').convert("RGBA")
        width, height = original.size
        
        txt = Image.new('RGBA', original.size, (255, 255, 255, 0))
        font = ImageFont.truetype("arial.ttf", 48)
        draw = ImageDraw.Draw(txt)

        text_width, text_height = draw.textsize(watermark_text, font=font)
        position = ((width - text_width) // 2, (height - text_height) // 2)
        draw.text(position, watermark_text, fill=(255, 255, 255, 180), font=font)

        watermarked = Image.alpha_composite(original, txt)
        watermarked.convert("RGB").save(output_image_path)

    except UnidentifiedImageError:
        raise UnidentifiedImageError(f"Cannot identify image file: {input_image_path}")
