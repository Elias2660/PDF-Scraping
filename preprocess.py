import PyPDF2

def extract_text(pdf_file) -> str:
    pdf = PyPDF2.PdfReader(pdf_file)
    text = []
    for page in pdf.pages:
        text.append(page.extract_text())
    return "\n".join(text)

print(extract_text("docs/2011_Yale_Advanced.pdf").replace("\n",""))

# First find all the pdf files in the directory

# Then prompt the user for the regex, level, year, and contest 
# when given the regex, also wite the extracted text in order to have the user be able to find the specified regex

# save all of that in a CSV file (text, the regex, year, level and contest)