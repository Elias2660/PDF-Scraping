from pdfminer.high_level import extract_text
import re

# Extract text from the PDF
pdf_path = "docs/Yale+Certamen+2020+-+Intermediate+Tournament.pdf"
text = extract_text(pdf_path)

# Normalize newlines
cleaned_text = text.replace("-\n", "")  # Merge words split with hyphens
cleaned_text = cleaned_text.replace("\n\n", " ")  # Replace newlines with spaces
cleaned_text = " ".join(cleaned_text.split())  # Remove extra spaces
while True:
    match = re.search(r"\d\.", cleaned_text)
    if match:
        index = match.start() + 1
    else:
        break
    if (
        index < 4
        or index == len(cleaned_text) - 1
        or cleaned_text[index - 4 : index].__contains__("\n")
    ):
        break
    j = index - 1
    while j >= 0 and cleaned_text[j].isnumeric():
        if j > 0 and cleaned_text[j - 1] == "B":
            break
        j -= 1
    else:
        cleaned_text = cleaned_text[: j + 1] + "\n" + cleaned_text[j + 1 :]
    cleaned_text = cleaned_text[:index] + "\n" + cleaned_text[index + 1 :]

print(cleaned_text)

import pandas as pd
import numpy as np

#  NEXT STEPS
"""  
Role data  -> 
[Question, 
Question Answer, 
Bonus 1, 
Bonus 1 Answer,
Bonus 2,
Bonus 2 Answer Difficulty, 
Topic, Year, Contest, Round
(possibly level, such as prelims, finals, etc.)]
]

"""
