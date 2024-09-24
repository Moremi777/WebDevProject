from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
#from PyPDF2 import PdfReader, PdfWriter


def add_pdf_watermark(input_pdf_path, output_pdf_path, watermark_pdf_path):
    pdf_reader = PdfReader(input_pdf_path)
    pdf_writer = PdfWriter()
    watermark_pdf_path = "O:\\CMPG 323 IT DEVELOPMENT\\backend\\WebDevProject\\share2teach\\static\\nwu-licence.pdf"

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
        # Open the original image
        original = Image.open(input_image_path).convert("RGBA")
        width, height = original.size
        
        # Create a new transparent layer for watermarking
        txt = Image.new('RGBA', original.size, (255, 255, 255, 0))

        # Choose a font and size for the watermark
        font = ImageFont.truetype("arial.ttf", 48)  # Increase font size for visibility
        draw = ImageDraw.Draw(txt)

        # Position the watermark in the center of the image
        text_width, text_height = draw.textsize(watermark_text, font=font)
        position = ((width - text_width) // 2, (height - text_height) // 2)

        # Draw watermark with a higher opacity for better visibility
        draw.text(position, watermark_text, fill=(255, 255, 255, 180), font=font)  # White color, increased opacity

        # Combine the original image with the watermark
        watermarked = Image.alpha_composite(original, txt)

        # Save the result as a JPEG or PNG depending on the original format
        watermarked.convert("RGB").save(output_image_path)

    except UnidentifiedImageError:
        raise UnidentifiedImageError(f"Cannot identify image file: {input_image_path}")
