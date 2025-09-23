# Selenium Signup Automation Script

This repository contains a Python script to automate testing of the signup flow on [Authorized Partner Signup Page](https://authorized-partner.netlify.app/login). The script performs both positive and negative test cases, including validations, password policy checks, SQL injection attempts, and successful user registration.

---

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Creating Virtual Environment](#creating-virtual-environment)
- [Running the Script](#running-the-script)
- [Running with Pytest and Generating Report](#running-with-pytest-and-generating-report)
- [Test Cases Implemented](#test-cases-implemented)
- [Test Data / Accounts](#test-data--accounts)
- [Notes](#notes)
- [Screenshots](#screenshots)
- [License](#license)

---

## Features

- Navigate from login page to signup form
- Fill signup form dynamically with test data
- Validate form fields for:
  - Empty submissions
  - Password mismatch
  - Invalid email format
  - Short passwords
  - Missing special characters or numbers
  - Invalid phone numbers
  - Duplicate emails
- Test for SQL injection vulnerabilities
- Perform valid signup and check for success messages
- Automatically detect validation errors using:
  - `aria-invalid` attributes
  - Error styling (border-destructive)
  - Visible error messages
- Saves screenshots for failed steps

---

## Prerequisites

- **Python 3.10+**
- **Google Chrome** installed
- **ChromeDriver** corresponding to your Chrome version. Download from [here](https://chromedriver.chromium.org/downloads)
- Python packages:
  - `selenium`
  - `pytest`
  - `pytest-html`
  - `time` (built-in)

Install required packages using pip:

```bash
pip install selenium pytest pytest-html
```

---

## Setup Instructions

1. Clone this repository:

```bash
git clone <repository_url>
cd <repository_folder>
```

2. Ensure Chrome and ChromeDriver are installed and added to your system PATH.

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Creating Virtual Environment

It is recommended to use a virtual environment to avoid conflicts:

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

- **Windows (Command Prompt):**
```bash
venv\Scripts\activate
```
- **Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```
- **Linux/macOS:**
```bash
source venv/bin/activate
```

3. Install dependencies inside the virtual environment:

```bash
pip install selenium pytest pytest-html
```

4. To deactivate the environment when done:

```bash
deactivate
```

---

## Running the Script

Run the script directly using Python:

```bash
python signup_automation_script.py
```

or if using a separate test function:

```bash
python -c "from signup_automation import test_signup_flow; test_signup_flow()"
```

**Note:** The script will open a Chrome browser, execute the tests sequentially, and close the browser at the end.

---

## Running with Pytest and Generating Report

1. Create a test file (if not already created, e.g., `test_signup.py`) with the following content:

```python
from signup_automation import automate_signup

def test_signup_flow():
    automate_signup()
```

2. Run tests using pytest and generate an HTML report:

```bash
pytest test_signup.py --html=report.html --self-contained-html
```

3. Open the generated `report.html` in a browser to view detailed test results.

---

## Test Cases Implemented

### Negative Test Cases
1. Empty form submission
2. Password mismatch
3. Invalid email format
4. Short password (<8 characters)
5. Password without special character
6. Password without number
7. Invalid phone number
8. Duplicate email
9. SQL injection attempt in first name field

### Positive Test Case
- Valid signup with unique email and correct credentials

---

## Test Data / Accounts

- Emails are dynamically generated using timestamps to ensure uniqueness:

```python
testuser_<timestamp>@example.com
```

- Passwords used for testing: `Test@12345`  
- Phone numbers for testing: `9800000000`  

---

## Notes

- Ensure your network allows access to the signup page.
- Selenium WebDriver may open multiple tabs or pop-ups depending on the site behavior.
- Screenshots of failures are automatically saved in the current directory:
  - `signup_failed.png`
  - `sql_injection_failure.png`
  - `unexpected_error.png`
- Adjust `WebDriverWait` timeout values if page loads slower than expected.
- Virtual environments are recommended to avoid dependency conflicts.
- Pytest HTML report provides a detailed summary of each test execution.

---

## Screenshots

Screenshots are taken automatically for failed test cases.  
Example:

```
signup_failed.png
sql_injection_failure.png
unexpected_error.png
```

---

**Author:** Laxman Sharma