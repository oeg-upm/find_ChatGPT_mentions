import os
import csv
import re
import json

def preprocess_mention(mention):
    return " ".join(mention.strip().split())

def extract_section(content, start_index, end_index):
    section_start = content.rfind("\\section{", 0, start_index)
    section_end = content.find("}", section_start)
    if section_start != -1 and section_end != -1:
        return content[section_start + 9:section_end]
    return "Section Not Found"

def is_within_comment(content, index):
    # Check if the index is within a line starting with %
    newline_index = content.rfind("\n", 0, index)
    if newline_index != -1:
        line = content[newline_index:index].strip()
        if line.startswith("%"):
            return True
    return False

def extract_paragraph(content, start_index, end_index):
    # Find the paragraph containing the mention
    paragraph_start = content.rfind("\n", 0, start_index) + 1
    paragraph_end = content.find("\n", end_index)
    return content[paragraph_start:paragraph_end].strip()

def search_for_variants(base_dir, output_csv, output_json):
    # Define regular expression to search for
    CHATGPT_REGEX = re.compile(r'chat[ \-_]{0,1}gpt', re.IGNORECASE)
    COPILOT_REGEX = re.compile(r'co[ \-_]{0,1}pilot', re.IGNORECASE)

    patterns = [CHATGPT_REGEX, COPILOT_REGEX]

    mentions = {}

    for subdir, _, files in os.walk(base_dir):
        for file in files:
            if file == "merged.tex":
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern in patterns:
                        matches = pattern.finditer(content)
                        for match in matches:
                            mention = match.group(0)
                            mention = preprocess_mention(mention)
                            is_comment = is_within_comment(content, match.start())
                            if mention not in mentions:
                                mentions[mention] = []
                            section = extract_section(content, match.start(), match.end())
                            paragraph = extract_paragraph(content, match.start(), match.end())
                            mentions[mention].append({"file": file_path, "section": section, "comment": is_comment, "context": paragraph})

    # Write results to CSV file
    with open(output_csv, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['mention', 'appearances'])
        for mention, files in mentions.items():
            writer.writerow([mention, len(files)])

    print(f"CSV file '{output_csv}' created successfully.")

    # Write appearances with sections, comment status, and context to JSON file
    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(mentions, json_file, ensure_ascii=False, indent=4)

    print(f"JSON file '{output_json}' created successfully.")

    # Print summary
    print("\nSummary of Appearances:")
    count = 0
    for mention, files in mentions.items():
        count += len(files)
        print(f"'{mention}': {len(files)} appearance(s) in {len(set([entry['file'] for entry in files]))} paper(s)")
    
    print(f"There is a total of {count} mentions")

if __name__ == "__main__":
    base_dir = "sources"
    output_csv = "mentions.csv"
    output_json = "appearances_sections_comments.json"
    search_for_variants(base_dir, output_csv, output_json)
