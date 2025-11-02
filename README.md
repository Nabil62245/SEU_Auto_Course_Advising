# SEU Course Advising Automation

A simple Python script to automate fetching offered course sections and attempting to add selected courses for advising on the SEU UMS system. This repository contains the script `SEU_Auto_Course_Advising.py` and example usage. Use of this code must follow the SEU terms of service and applicable laws.

> Educational purpose only. This tool is provided for learning and automation demonstration. Do not use it to abuse or circumvent any university systems, policies, or rate limits. Use responsibly.

## Features

- Log in to SEU UMS using username and password (via API).
- Fetch offered course sections for the logged-in student.
- Support selecting courses interactively or providing a pre-defined list to add automatically.
- Attempt to add each selected course until all are added or retries exhaust.

## Requirements

- Python 3.8+
- `requests` Python package

## Installation

Open PowerShell (Windows) and run:

```powershell
python -m pip install --user requests
```

(Or use `pip install requests` in your preferred environment.)

## Files

- `SEU_Auto_Course_Advising.py` — main script that performs login, fetching offered courses, and adding selected courses.
- `README.md` — this file.

## How it works (high level)

1. The script prompts for your SEU username and password (or accepts them when provided programmatically).
2. It calls the UMS sign-in endpoint and obtains an access token.
3. With the token, it fetches the advising table (offered sections).
4. The script either prompts you to enter desired course codes (like `MAT223.3`) or accepts a `course_to_add` list to run non-interactively.
5. It iteratively posts add/drop requests for each selected course until they are successfully added or retries continue.

## Usage

Interactive (recommended to see offered sections and pick courses manually):

```powershell
python SEU_Auto_Course_Advising.py
```

You will be prompted to enter:
- `Enter your SEU username:`
- `Enter your SEU password:`

Then follow prompts to provide course codes and sections.

Non-interactive example (edit the script):

1. Open `SEU_Auto_Course_Advising.py` and set `course_to_add` near the bottom, for example:

```python
course_to_add = ["EEE181.5", "MAT241.4", "ENG103.18", "CSE241.5"]
```

2. Run the script (you can also pass username/password by editing the `USERNAME` and `PASSWORD` variables in the file):

```powershell
python SEU_Auto_Course_Advising.py
```

## Important notes and cautions

- Credentials: This script requires your SEU username and password. Treat these credentials securely. Avoid committing them into version control.
- API behavior: This script interacts with SEU's UMS API endpoints. Excessive or abusive automated requests may violate university policies. Use sensible delays and limits.
- Tokens and security: The script uses the access token returned by the UMS sign-in endpoint. Do not share tokens.
- Educational use only: This project is provided for study and automation learning purposes only. Do not use it to circumvent enrollment controls or to perform actions you are not authorized to do.

## Troubleshooting

- If `requests` is not installed, install it with `pip install requests`.
- If login fails, verify credentials and that the UMS API endpoint is reachable from your network.
- If the offered course list is empty, ensure you are enrolled and the advising window is open.

## License & Disclaimer

Provided "as-is" for educational purposes only. Use at your own risk.

This repository is licensed under the MIT License. See below for a short summary: you may reuse and modify the code, but the authors provide no warranty.

---

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY.
