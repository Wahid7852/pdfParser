#!/bin/bash

pdf_directory="pdfs"
api_url="https://edmonton-site-penalties-shift.trycloudflare.com/parse_document/pdf"
regex_pattern='(?<=\n)(.*?)(?=## 1 )|##\s\d+[\.\d]*\s.*?(?=\n##\s\d+|\Z)'

for pdf_path in "$pdf_directory"/P001.pdf; do
    filename=$(basename "$pdf_path" .pdf)

    response=$(curl -X POST -F "file=@$pdf_path" "$api_url")
    if [[ $? -eq 0 && ! -z "$response" ]]; then
        parsed_text=$(echo "$response" | jq -r '.text')

        sections=$(echo "$parsed_text" | grep -oP "$regex_pattern")
        csv_output="$pdf_directory/$filename.csv"
        echo "Heading,Content" > "$csv_output"

        while IFS= read -r section; do
            escaped_section=$(echo "$section" | sed 's/,/\\,/g')
            if [[ -n "$escaped_section" ]]; then
                echo "$filename,$escaped_section" >> "$csv_output"
            fi
        done <<< "$sections"

        echo "CSV file created for $filename at $csv_output"
    else
        echo "Failed to parse $pdf_path"
    fi
done
