# importing required classes
from PyPDF2 import PdfReader
import pdfplumber
from pprint import pprint
import os


def join_lines(page_list):
    # if the line is empty, remove it, join it with the next line
    # if the line is not empty and not caps lock, join it with the next line
    ...


# creating a pdf reader object
file_list = os.listdir("docs")
for file in file_list:
    with pdfplumber.open(os.path.join("docs", file)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        text = text.replace("\n\n", "\n")
        text = text.replace(" and ", " AND ")
        text = text.replace("\u200b", "")
        while "  " in text:  # removing double spaces
            text = text.replace("  ", " ")
        text_list = text.split("\n")
        to_be_removed = []
        for i in range(len(text_list)):
            if text_list[i].replace(" ", "") == "":
                to_be_removed.append(i)
        text_list = [
            text_list[i] for i in range(len(text_list)) if i not in to_be_removed
        ]
        q_list = []
        started = False
        current_q = ""
        for i in range(len(text_list)):
            if text_list[i].__contains__("Preliminary"):
                started = True
            elif started and text_list[i].upper() != text_list[i]:
                current_q += text_list[i] + " "
            elif (
                started
                and text_list[i].strip()[0].isnumeric()
                and not (text_list[i].replace(" and ", " AND ").replace(" ", ""))
                .strip()
                .upper()
                == (text_list[i].replace(" and ", " AND ").replace(" ", "").strip())
            ):
                print("hit")
                q_list.append(
                    current_q.replace("'", "")
                    .replace("\n", " ")
                    .replace(" AND", " and ").strip()
                )
                current_q = text_list[i]
            elif started and (
                text_list[i].replace(" and ", " AND ").replace(" ", "")
            ).strip().upper() == (
                text_list[i].replace(" and ", " AND ").replace(" ", "").strip()
            ):
                q_list.append(
                    current_q.replace("'", "")
                    .replace("\n", " ")
                    .replace(" AND ", " and ").strip()
                )
                q_list.append(
                    text_list[i]
                    .replace("  ", "")
                    .replace("'", "")
                    .replace("\n", " ")
                    .replace(" AND ", " and ").strip()
                )
                current_q = ""

        for item in q_list:
            print(item)

        print("\n")
