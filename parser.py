import re
import csv
import requests
import os

def parse_pdf(pdf_path, api_url):
    with open(pdf_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(api_url, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to parse {pdf_path}, status code: {response.status_code}")
            return None

regex_pattern = r"(?<=\n)(.*?)(?=## 1 )|##\s\d+[\.\d]*\s.*?(?=\n##\s\d+|\Z)"
api_url = "https://das-scales-lopez-casio.trycloudflare.com/parse_document/pdf" # not static, bound to change as per Local LLM-Parser
pdf_directory = "pdfs/"
csv_directory = "csvs/"

for file in os.listdir(pdf_directory):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, file)
        response_data = parse_pdf(pdf_path, api_url)

        if response_data and 'text' in response_data:
            parsed_text = response_data['text']
            matches = re.finditer(regex_pattern, parsed_text, re.DOTALL)
            sections = {}
            for match in matches:
                content = match.group(0).strip()

                if content.startswith("##"):
                    if "\n" in content:
                        heading, body = content.split("\n", 1)
                        sections[heading.strip()] = body.strip()
                    else:
                        sections[content.strip()] = ""
                else:
                    sections["Title"] = content.strip()

            output_csv = os.path.join(csv_directory, f"{file[:-4]}.csv")
            with open(output_csv, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                headings = list(sections.keys())
                writer.writerow(headings)

                content_row = [sections.get(heading, "") for heading in headings]
                writer.writerow(content_row)

            print(f"CSV file created for {file} at {output_csv}")
        else:
            print(f"Could not parse {pdf_path}")
