import PyPDF2
import os
from openai import OpenAI
from dotenv import load_dotenv

HBLK = "\033[30m"
HRED = "\033[31m"
BHRED = "\033[1;31m"
BHBLUE = "\033[1;34m"
HGRN = "\033[32m"
HYEL = "\033[33m"
HBLU = "\033[34m"
HMAG = "\033[35m"
HCYN = "\033[36m"
HWHT = "\033[37m"
GREY = "\033[90m"
reset = "\033[0m"

files = os.listdir("docs")

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

incorrect_answers, correct_answers = 0, 0

for file in files:
    pdf_path = os.path.join("docs", file)

    load_dotenv()

    open_pdf_file = open(pdf_path, "rb")
    text = ""

    read_pdf = PyPDF2.PdfReader(open_pdf_file)
    for i in range(len(read_pdf.pages)):
        if read_pdf.is_encrypted:
            read_pdf.decrypt("")
            text += read_pdf.pages[i].extract_text() + "\n"

        else:
            text += read_pdf.pages[i].extract_text() + "\n"

    client = OpenAI(api_key=os.getenv("API_KEY", ""))

    context = "System: You are a helpful assistant trying to reformat data, only returning the data requested, not anything else.\n"

    questions = "1,2,3,4,5,6,7,8,9,10,11, 12,13,14,15,16,17,18,19,20".split(",")
    questions.append("Bonus HISTORY")
    questions.append("Bonus MYTHOLOGY")
    questions.append("Bonus LANGUAGE")

    import pandas as pd

    rounds = [
        "Preliminary Round 1",
        "Preliminary Round 2",
        "Preliminary Round 3",
        "Semifinals",
        "Finals",
    ]

    for ROUND in rounds:
        for question in questions:
            print()
            print(
                f"---- Question {HRED}{question}{reset} of Round {HBLU}{ROUND}{reset} of file {HCYN}{pdf_path}{reset} ----"
            )

            assistant_prompt = f"""


                Use your best intution to extract the questions from the data, but given your knowledge try your best.
                
                - for difficulty, use either "Beginner", "Intermediate", or "Advanced", and extract from the name of the file, for example docs/Yale+Certamen+2020+-+Intermediate+Tournament.pdf would be "Intermediate"
                - for contest name, extract from the name of the contest, for example docs/Yale+Certamen+2020+-+Intermediate+Tournament.pdf would be "Yale Certamen 2020", otherwise get it from the materials in the pdf
                
                - also try to remove the labels of the questions such as 'B1' or '1'
                - REPLACE ALL COMMAS IN THE QUESTION SECTIONS, BUT NOT THE COMMAS SEPARATING THE PARTS OF THE QUESTION, with 'CC' in the format of the following so that it would be easier to split the output into a list
                - Comma replacement only works within each option, but not between the options, for example, don't put a 'CC' between the question and the answer, only if there is a comma within the question or answer
                - REMEMBER TO place a comma separating a question and its answers!, don't put unnessary quotes around the answers
                - Also remember to not output anything besides the formatted info, no extra information is needed 
                
                Please analyze and output the correct format this question for tossup question {question} for round {ROUND} as a row divided by commas in the following format: Main Question, Main Question Answer, Bonus Question 1, Bonus Question 1 Answer, Bonus Question 2, Bonus Question 2 Answer, Difficulty Level, Topic, Year, Contest Name, Round
                
                -------
                
                Here is a formatted EXAMPLE QUESTION: 
                From what Latin verb with what meaning are the English words “adroitCC” “incorrigibleCC” and “regiment” derived?, REGŌ (REGERE ) = (TO / I) RULE, From what Latin verb with what meaning is “surrogate” derived?, ROGŌ (ROGĀRE) = (TO / I) ASK, From what Latin verb with what meaning is “risible” derived?, RĪDEŌ (RĪDĒRE) = (TO / I) LAUGH, Grammar Derivatives, YEAR, CONTEST, LEVEL
                
                This is also CORRECT:
                Let's go to AthensCC, EAMUS ATHĒNĀS, Say in LatinCC "If only I had believed youCC", UTINAM TIBI CRĒDIDISSEM, Say in LatinCC "What were we to doCC" , QUID AGERĒMUS / FACERĒMUS, Advanced, Lang Latin, 2013, Yale Invitational, Preliminary Round 1
                
                This is INCORRECT because it doesn't split between the questions and answers
                'What fruit did the Romans call malum punicum? POMEGRANATE', 'What fruit did the Romans call malum persicum? PEACH', 'What fruit did the Romans call cerasus? CHERRY', 'Advanced', 'Relevant Term', '2013', 'Yale Certamen Invitational', 'Round 1'
                
                This is INCORRECT because it replaces the commas between the formatted list options
                'Quid Anglicē significat “carcer”CC  PRISON / STARTING GATECC Quid Anglicē significat “cinis”CC ASHES / DEATH / RUINCC Quid Anglicē significat “carīna”CC KEEL / SHIPCC Advanced, Vocabulary, 2013, Yale Certamen Invitational, Preliminary Round 1'
                
                -------
                
                this is the format of the output for the question asked for (remember to not replace the commas separating each part of the options for the list): Main Question, Main Question Answer, Bonus Question 1, Bonus Question 1 Answer, Bonus Question 2, Bonus Question 2 Answer, Difficulty Level, Topic, Year, Contest Name, Round
               
               \n"""

            initial_model = "gpt-4o"
            print(f"Performing initial formatting prompt with {initial_model}")
            original_response = client.chat.completions.create(
                model=initial_model,
                messages=[
                    {"role": "user", "content": context},
                    {"role": "user", "content": assistant_prompt},
                    {"role": "user", "content": text.replace("\n", " ")},
                ],
            )

            origional_output = original_response.choices[0].message.content

            if origional_output or origional_output != "None":
                print(f"{HCYN}Origional Output{reset}: {origional_output}")
                options = [
                    a.replace("CC", ",").replace("  ", " ").strip()
                    for a in origional_output.strip().split(",")
                ]

                if len(options) != len(df.columns):
                    checker_model = "o1-mini"
                    print(
                        f"Wrong number of options {HRED}({len(options)}){reset}, retrying with {HCYN}{checker_model}{reset}"
                    )
                    print(f"{HRED}Incorrect options{reset}: {options}")
                    response = client.chat.completions.create(
                        model=checker_model,
                        messages=[
                            {"role": "user", "content": context + "\n"},
                            {
                                "role": "user",
                                "content": f"""
                                
                                {assistant_prompt}
                                
                                - A big problem is that the the earlier model replaces commas in the question with "CC" which causes them to be treated as a single option, or doesn't have any differentiation between the question and answer, which causes the output to be incorrect (especially leading the options to be less than correct)
                                
                                - if there are more options than correct, then it probably is because they forgot to replace a comma with a 'CC'
                                
                                Remember to output the response as reformated from the below as needed to match the format of the examples, REDUCE the number of split parts, which was at {len(options)} which is NOT EQUAL to {len(origional_output.split(','))}
                                
                                
                                {origional_output}
                                """,
                            },
                        ],
                    )
                    revised_response = response.choices[0].message.content
                    print(f"{HGRN}Revised Response{reset}: {revised_response}")
                    options = [
                        a.replace("CC", ",").replace("  ", " ").strip()
                        for a in revised_response.strip().split(",")
                    ]
                    if len(options) != len(df.columns):
                        second_checker_model = "o1-mini"
                        print(
                            f"The wrong number of options (with length of {HRED}{len(options)}{reset} compared to the correct length of {HGRN}{len(df.columns)}{reset}) was returned, re-trying with {HCYN}{second_checker_model}{reset}"
                        )
                        response = client.chat.completions.create(
                            model=second_checker_model,
                            messages=[
                                {"role": "user", "content": context + "\n"},
                                {
                                    "role": "user",
                                    "content": f"""
                                
                                {assistant_prompt}
                                                                
                                Remember to output the response as reformated from the below as needed to match the format of the examples, REDUCE the number of split parts, which was at {len(options)} which is NOT EQUAL to {len(origional_output.split(','))}
                                
                                {revised_response}
                                """,
                                },
                            ],
                        )
                        second_revised_response = response.choices[0].message.content
                        print(
                            f"{HGRN}Revised Response{reset}: {second_revised_response}"
                        )
                        options = [
                            a.replace("CC", ",").replace("  ", " ").strip()
                            for a in second_revised_response.strip().split(",")
                        ]
                        if len(options) != len(df.columns):
                            print(
                                f"The wrong number of options (with length of {HRED}{len(options)}{reset} compared to the correct length of {HGRN}{len(df.columns)}){reset} was returned, writing to file"
                            )
                            print(f"{HRED}Incorrect options:{reset} {options}")
                            incorrect_answers += 1
                            with open("Incorrect_Questions.txt", "a") as f:
                                f.write(
                                    f"Question {question} of round {ROUND} from pdf {pdf_path} is incorrect: {revised_response}\n"
                                )
                            continue
                        else:
                            print(f"{HGRN}Correct options{reset}: {options}")

                for i in range(len(options)):
                    options[i] = options[i].replace("CC", ",")
                options[-1] = ROUND
                print(
                    f"Option Length: {HCYN}{len(options)}{reset}, length of df.columns: {HCYN}{len(df.columns)}{reset}"
                )
                print(f"Options: {options}")

                if len(options) == len(df.columns):
                    correct_answers += 1
                    df.loc[len(df)] = options
                else:
                    print(
                        f"Skipping question {question} due to mismatched column length"
                    )
                print(df)

        df.to_csv("output.csv", index=False)

print(
    f"Incorrect Answers: {HRED}{incorrect_answers}{reset}, Correct Answers: {HGRN}{correct_answers}{reset}"
)
