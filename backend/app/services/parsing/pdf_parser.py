import fitz
import io

# External service that actually parses the pdf with help of PyMuPDF and then sends back to function
def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    try:
        pdf_document = fitz.open(stream = file_bytes, filetype = "pdf")
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text") + "\n"
        
        pdf_document.close()
        return text.strip()

    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""
        
