import streamlit as st
import pdfkit
import markdown
import os
import tempfile
from PyPDF2 import PdfReader

# Function to convert PDF to HTML using pdfkit
def pdf_to_html(pdf_file):
    # Save uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_file.read())
        temp_pdf_path = temp_pdf.name

    # Define output HTML file path
    html_file_path = temp_pdf_path.replace('.pdf', '.html')

    # Convert PDF to HTML using pdfkit
    try:
        pdfkit.from_file(temp_pdf_path, html_file_path)
    except Exception as e:
        st.error(f"Error converting PDF to HTML: {e}")
        return None

    # Read the generated HTML file
    with open(html_file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    return html_content

# Function to convert HTML to Markdown using markdown library
def html_to_markdown(html_content):
    md_content = markdown.markdown(html_content)
    return md_content

# Streamlit App
def main():
    st.title("Resume Converter: PDF to HTML & Markdown")
    
    # Upload PDF file
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

    if uploaded_file is not None:
        st.write("File uploaded successfully!")

        # Convert PDF to HTML
        html_content = pdf_to_html(uploaded_file)
        
        if html_content:
            st.subheader("HTML Version:")
            st.code(html_content, language='html')

            # Convert HTML to Markdown
            md_content = html_to_markdown(html_content)
            st.subheader("Markdown Version:")
            st.code(md_content, language='markdown')

if __name__ == "__main__":
    main()
