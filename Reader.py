# importing required classes
from pypdf import PdfReader

# creating a pdf reader object
reader = PdfReader('Yale+Certamen+2020+-+Intermediate+Tournament.pdf')

# printing number of pages in pdf file
print(len(reader.pages))

# creating a page object
# page = reader.pages[0]

for page in reader.pages:
    print(page.extract_text())

# extracting text from page