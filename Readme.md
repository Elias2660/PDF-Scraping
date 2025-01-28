# Project PDF READER

# for further reading: 
https://brainhub.eu/library/pdf-insights-aws-textract-openai

This repository explores various approaches to parsing PDFs for text extraction and question generation. It demonstrates attempts at integrating multiple scripts, including GPT-specific workflows, to process and structure data from Certamen PDFs.

## Overview
1. Experimented with libraries such as pdfplumber and PyPDF2.  
2. Attempted to handle text concatenation, removal of extra spacing, and multi-line parsing.  
3. Utilized GPT-based functions to transform parsed data into structured CSV files.

## Conclusion
Despite numerous trials, this quest has not been able to fully overcome GPT’s unreliability in providing a consistently effective PDF parser.
### Additional Details
A structured pipeline was used to parse PDFs in segmented chunks. Libraries like pdfplumber were employed to extract text, while custom scripts integrated GPT-based logic for data formatting. Iterative refinements focused on normalizing whitespace, handling multiline passages, and reducing inconsistencies in output generation.