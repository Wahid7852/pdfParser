import re
import csv
import requests
import os

# Function to parse a PDF using the provided API endpoint
def parse_pdf(pdf_path, api_url):
    with open(pdf_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(api_url, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to parse {pdf_path}, status code: {response.status_code}")
            return None

# Full regex pattern for splitting sections
regex_pattern = r"(?<=\n)(.*?)(?=## 1 )|##\s\d+[\.\d]*\s.*?(?=\n##\s\d+|\Z)"

# API endpoint for parsing PDF
api_url = "https://edmonton-site-penalties-shift.trycloudflare.com/parse_document/pdf"

# Directory where the PDFs are stored
pdf_directory = "pdfs"

# Loop through each PDF file in the directory
for file in os.listdir(pdf_directory):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, file)
        # Parse the PDF using the API
        response_data = parse_pdf(pdf_path, api_url)

        if response_data and 'text' in response_data:
            parsed_text = response_data['text']
            
            # Apply regex to extract sections
            matches = re.finditer(regex_pattern, parsed_text, re.DOTALL)

            # Process matches into a dictionary to store content under each heading
            sections = {}
            for match in matches:
                content = match.group(0).strip()

                # Ensure there is a newline to split, otherwise, treat it as a title
                if content.startswith("##"):
                    if "\n" in content:
                        heading, body = content.split("\n", 1)
                        sections[heading.strip()] = body.strip()
                    else:
                        sections[content.strip()] = ""
                else:
                    sections["Title"] = content.strip()

            # Write the parsed content to a CSV
            output_csv = os.path.join(pdf_directory, f"{file[:-4]}.csv")
            with open(output_csv, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Write the headings as the top row
                headings = list(sections.keys())
                writer.writerow(headings)

                content_row = [sections.get(heading, "") for heading in headings]
                writer.writerow(content_row)

            print(f"CSV file created for {file} at {output_csv}")
        else:
            print(f"Could not parse {pdf_path}")
