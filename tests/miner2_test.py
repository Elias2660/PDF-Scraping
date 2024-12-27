import pdfplumber
import pandas as pd

# Define output columns
columns = [
    "Main Question", "Main Question Answer", 
    "Bonus Question 1", "Bonus Question 1 Answer", 
    "Bonus Question 2", "Bonus Question 2 Answer", 
    "Difficulty Level", "Topic", "Year", 
    "Contest Name", "Round Number"
]

# Initialize data list
data = []

def parse_rounds(text, round_number):
    """
    Parse the text for a specific round and extract questions/answers.
    """
    lines = text.split("\n")
    current_row = {col: "" for col in columns}
    current_row["Round Number"] = round_number
    question_mode = False
    bonus_mode = None

    for line in lines:
        # Detect metadata
        if "2013 Yale Certamen Invitational" in line:
            current_row["Year"] = 2013
            current_row["Contest Name"] = "Yale Certamen Invitational"
        elif line.startswith("Round"):
            current_row["Round Number"] = line.split()[-1]
        
        # Detect Main Question
        if line.strip().isdigit():
            if question_mode or bonus_mode:
                data.append(current_row)
                current_row = {col: "" for col in columns}
                current_row["Round Number"] = round_number
            question_mode = True
            current_row["Main Question"] = ""
            current_row["Main Question Answer"] = ""
        
        # Fill in Main Question and Answer
        elif question_mode:
            if "?" in line:
                question, _, answer = line.partition("?")
                current_row["Main Question"] = question.strip()
                current_row["Main Question Answer"] = answer.strip()
                question_mode = False
            else:
                current_row["Main Question"] += f" {line.strip()}"

        # Detect Bonus Questions
        elif line.startswith("B1"):
            bonus_mode = "Bonus Question 1"
            question, _, answer = line.partition("?")
            current_row[bonus_mode] = question.strip()
            current_row[f"{bonus_mode} Answer"] = answer.strip()
        elif line.startswith("B2"):
            bonus_mode = "Bonus Question 2"
            question, _, answer = line.partition("?")
            current_row[bonus_mode] = question.strip()
            current_row[f"{bonus_mode} Answer"] = answer.strip()

    if current_row not in data:
        data.append(current_row)

# Process the PDF
with pdfplumber.open("./docs/yale_2013_advanced.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if "Round" in text:
            round_number = text.split("Round")[-1].split()[0]
        else:
            round_number = "Unknown"
        parse_rounds(text, round_number)

# Convert to DataFrame
df = pd.DataFrame(data, columns=columns)

# Save as CSV
output_file = "parsed_certamen_questions_correct.csv"
df.to_csv(output_file, index=False)

print(f"Data successfully parsed and saved to {output_file}")
