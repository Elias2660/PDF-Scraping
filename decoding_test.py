import PyPDF2

pdf_path = "docs/Yale+Certamen+2020+-+Intermediate+Tournament.pdf"


open_pdf_file = open(pdf_path, "rb")
text = ""

read_pdf = PyPDF2.PdfReader(open_pdf_file)
for i in range(len(read_pdf.pages)):
    if read_pdf.is_encrypted:
        read_pdf.decrypt("")
        text += read_pdf.pages[i].extract_text()

    else:
        text += read_pdf.pages[i].extract_text()


import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY", ""))

pdf_path = "docs/Yale+Certamen+2020+-+Intermediate+Tournament.pdf"

with open(pdf_path, "rb") as f:
    file_content = f.read()

context = "You are a helpful assistant trying to reformat data."


questions = "1,2,3,4,5,6,7,8,9,10,11, 12,13,14,15,16,17,18,19,20".split(",")
questions.append("Bonus HISTORY")
questions.append("Bonus MYTHOLOGY")
questions.append("Bonus LANGUAGE")


import pandas as pd

df = pd.DataFrame(
    columns=[
        "Question",
        "Answer",
        "Bonus 1",
        "Bonus 1 Answer",
        "Bonus 2",
        "Bonus 2 Answer",
        "Difficulty Level",
        "Topic",
        "Year",
        "Contest",
        "Round",
    ]
)


for question in questions:
    
    ROUND = "Preliminary Round 1"
    
    assistant_prompt = (
        f"""
        -----
        
        Here is a formatted EXAMPLE QUESTION: 
        From what Latin verb with what meaning are the English words “adroitCC” “incorrigibleCC” and “regiment” derived?, REGŌ (REGERE ) = (TO / I) RULE, From what Latin verb with what meaning is “surrogate” derived?, ROGŌ (ROGĀRE) = (TO / I) ASK, From what Latin verb with what meaning is “risible” derived?, RĪDEŌ (RĪDĒRE) = (TO / I) LAUGH, Grammar Derivatives, YEAR, CONTEST, LEVEL
        
        -------
        
        Please analyze and output the correct format this question for tossup question {question} for round {ROUND} as a row divided by commas; REPLACE ALL COMMAS IN ALL QUESTIONS (BUT NOT THE COMMAS SEPARATING THE PARTS OF THE QUESTION) with 'CC' in the format of the following, also try to remove the labels of the questions, such as 'B1' or '1':\n
        
        Main Question, Main Question Answer, Bonus Question 1, Bonus Question 1 Answer, Bonus Question 2, Bonus Question 2 Answer, Difficulty Level, Topic, Year, Contest Name, Round\n"""
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": context},
            {"role": "user", "content": assistant_prompt},
            {"role": "user", "content": text.replace("\n", " ")},
        ],
    )

    r = response.choices[0].message.content

    print()
    print(f"---- Question {question} ----")
    if r or r != "None":
        initial_model = "gpt-4o"
        print(f"Performing initial formatting prompt with {initial_model}")
        response = client.chat.completions.create(
            model=initial_model,
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": assistant_prompt},
                {
                    "role": "user",
                    "content": f"Remember to reformat as needed to match the format of the examples, reducing the number of split parts equals 11, currently there are {len(response.choices[0].message.content.split(','))}. Output so that this data can be used to create a row in a CSV file – do not give anything other than the data needed to create the row.",
                },
                {"role": "user", "content": response.choices[0].message.content},
            ],
        )
        origional_output = response.choices[0].message.content

        options = [
            a.replace("CC", ",").replace("\n", " ").replace("  ", " ").strip()
            for a in origional_output.strip().split(",")
        ]
        if len(options) != len(df.columns):
            print(f"Wrong number of options ({len(options)}), retrying with o1-preview")
            response = client.chat.completions.create(
                model="o1-preview",
                messages=[
                    {"role": "user", "content": context + "\n"},
                    {
                        "role": "user",
                        "content": assistant_prompt
                        + f"Remember to output the response as reformated as needed to match the format of the examples, REDUCE the number of split parts, which was at {len(options)} which is NOT EQUAL to {len(response.choices[0].message.content.split(','))}"
                        + response.choices[0].message.content,
                    },
                ],
            )
            revised_response = response.choices[0].message.content
            options = [
                a.replace("CC", ",").replace("\n", " ").replace("  ", " ").strip()
                for a in revised_response.strip().split(",")
            ]
            if len(options) != len(df.columns):
                print(
                    f"The wrong number of options (with length of {len(options)} compared to the correct length of {len(df.columns)}) was returned, skipping and writing question into a file"
                )
                with open("Incorrect_Questions.txt", "a") as f:
                    f.write(
                        f"Question {question} of round {ROUND} from pdf {pdf_path} is incorrect: {revised_response}\n"
                    )
                continue

        for i in range(len(options)):
            options[i] = options[i].replace("CC", ",")
        options[-1] = ROUND
        print("Option Length: ", len(options))
        print("Options: ", options)

        print("Length of df.columns: ", len(df.columns))
        if len(options) == len(df.columns):
            df.loc[len(df)] = options
        else:
            print(f"Skipping question {question} due to mismatched column length")
        print(df)

df.to_csv("output.csv", index=False)
