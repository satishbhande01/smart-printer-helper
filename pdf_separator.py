# pdf_separator.py
import fitz  # PyMuPDF

def is_color_page(page, threshold=0.001):
    pix = page.get_pixmap()
    if pix.n < 3:
        return False

    pixels = pix.samples
    total_pixels = pix.width * pix.height
    color_pixels = 0

    for i in range(0, len(pixels), pix.n):
        r, g, b = pixels[i:i+3]
        if r != g or g != b:
            color_pixels += 1
            if color_pixels / total_pixels > threshold:
                return True
    return False

def separate_pdf_by_color(input_pdf, threshold=0.001):
    doc = fitz.open(input_pdf)
    color_doc = fitz.open()
    bw_doc = fitz.open()

    for i in range(len(doc)):
        page = doc[i]
        if is_color_page(page, threshold=threshold):
            color_doc.insert_pdf(doc, from_page=i, to_page=i)
        else:
            bw_doc.insert_pdf(doc, from_page=i, to_page=i)

    color_output = "color_pages.pdf"
    bw_output = "bw_pages.pdf"

    color_saved = False
    bw_saved = False

    if len(color_doc) > 0:
        color_doc.save(color_output)
        color_saved = True
    if len(bw_doc) > 0:
        bw_doc.save(bw_output)
        bw_saved = True

    # Return based on what got saved
    if color_saved and bw_saved:
        return color_output, bw_output
    elif color_saved:
        return color_output, None
    elif bw_saved:
        return None, bw_output
    else:
        return None, None

