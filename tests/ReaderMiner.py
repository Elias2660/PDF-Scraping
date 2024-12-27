import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY", ""))

pdf_path = "docs/Yale+Certamen+2020+-+Intermediate+Tournament.pdf"

with open(pdf_path, "rb") as f:
    file_content = f.read()

context = "You are a helpful assisstant trying to convert raw data into text"

assistant_prompt = (
    """
    Fill out year from the contest name, and level from the level name.

TOPIC: Choose among the following options
'Daily Life', 'History', 'Literature', 'Mythology', 'Geography', 'Grammar Forms', 'Grammar Usage', 'Grammar Derivatives', 'Grammar Vocab', 'Grammar Listening Comprehension'

RETURN SOMETHING LINK THIS (see examples), like a list (remember to not include the titles, such as Bonus 1 Answer but only the actual answer as inthe examples below):
'Question, Question Answer, Bonus 1, Bonus 1 Answer, Bonus 2, Bonus 2 Answer, Topic, Year, Contest, Round'

The example questions are in the following format (unprocessed), and the output in on a lower line:
Example 1:
. From what Latin verb with what meaning are the English words “adroit,” “incorrigible,” and “regiment” derived? REGŌ (REGERE ) = (TO / I) RULE B1: From what Latin verb with what meaning is “surrogate” derived? ROGŌ (ROGĀRE) = (TO / I) ASK B2: From what Latin verb with what meaning is “risible” derived? RĪDEŌ (RĪDĒRE) = (TO / I) LAUGH 
From what Latin verb with what meaning are the English words “adroit,” “incorrigible,” and “regiment” derived?, REGŌ (REGERE ) = (TO / I) RULE, From what Latin verb with what meaning is “surrogate” derived?, ROGŌ (ROGĀRE) = (TO / I) ASK, From what Latin verb with what meaning is “risible” derived?, RĪDEŌ (RĪDĒRE) = (TO / I) LAUGH, Grammar Derivatives, YEAR, CONTEST, LEVEL

Example 1:
. “Swan-shaped” and “grey-haired” describe what group of women, sisters of the Gorgons who are most famous for sharing a single eye and tooth between themselves? B1: The Graeae were the children of what couple, who were also the parents of Echidna and Ladon? GRAEAE // GRAY SISTERS / WOMEN B2: Give the names of any two of the Graeae. PHORCYS and CETO TWO OF: ENYO, PE(M)PHREDO, OR DEINO 
“Swan-shaped” and “grey-haired” describe what group of women, sisters of the Gorgons who are most famous for sharing a single eye and tooth between themselves?, "GRAEAE // GRAY SISTERS / WOMEN", The Graeae were the children of what couple, who were also the parents of Echidna and Ladon?, "PHORCYS and CETO, Give the names of any two of the Graeae., TWO OF: ENYO, PE(M)PHREDO, OR DEINO", Mythology, YEAR , CONTEST, LEVEL

Do all of the questions in the following document separated by new lines. 
    """
    "Please analyze this text and provide the following information as a list of line-separated rows divided by commas:\n"
    + "Main Question,Main Question Answer,Bonus Question 1,Bonus Question 1 Answer,Bonus Question 2,Bonus Question 2 Answer,Difficulty Level,Topic,Year,Contest Name,Round Number"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": assistant_prompt},
        {"role": "user", "content": file_content.decode("utf-8")},
    ],
)
