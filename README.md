# Find ChatGPT Mentions


## Description

This project provides a Python script to detect mentions of ChatGPT and Copilot within LaTeX files. The key features are:

- Supports the detection of mentions using regular expressions, allowing for flexible pattern matching.

- Extracts the sections in which mentions occur within LaTeX files.

- Determines whether mentions are within LaTeX comments.

Outputs are saved in both CSV and JSON formats: 

- appearances_sections_comments.json, with the following structure:

```
{
    "Mention": [
        {
            "file": "path to the file when the mention is present",
            "section": "section of the file where the mention occurs",
            "comment": a boolean flag that indicates if the mention is within a comment
        },
}
```

- mentions.csv, with every different mention and the times it is present in the papers


## Usage

1. Place your LaTeX files inside a folder called "sources" in the root directory , following the structure of the example below:

```bash
$ cd sources
$ ls
2301.12169v1 2302.08664v3 2303.10131v1 2303.13729v2 2304.05766v1 2305.16365v1 2306.10019v1 2307.04291v1 2308.09637v2 2308.12079v1 2309.04197v1 2302.05564v1 2303.09727v1 2303.10439v2 2303.15684v1 2304.14628v2 
$ cd 2302.08664v3
$ ls
merged.tex
```

2. Run the command ```python search_chatgpt.py``` to start teh execution