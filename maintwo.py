import fitz  # PyMuPDF
from bs4 import BeautifulSoup

def pdf_to_html(pdf_path):
    pdf_document = fitz.open(pdf_path)
    html_content = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text = page.get_text("text")
        html_content += f"<p>{text}</p>"
    pdf_document.close()
    return html_content

pdf_path = "my_pdf.pdf"
html_output = pdf_to_html(pdf_path)

with open("output.html", "w", encoding="utf-8") as f:
    f.write(html_output)

def generate_html_markup(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    styled_html = soup.prettify()
    return styled_html

html_output = generate_html_markup(html_output)

with open("output_styled.html", "w", encoding="utf-8") as f:
    f.write(html_output)