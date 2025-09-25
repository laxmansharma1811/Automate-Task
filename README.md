# Selenium Signup Automation with PDF Test Report

This project automates the signup process on the [Authorized Partner Signup Page](https://authorized-partner.netlify.app/login) using Selenium WebDriver. It also generates a detailed PDF test report after execution.

---

## Table of Contents

* [Features](#features)
* [Prerequisites](#prerequisites)
* [Setup](#setup)
* [Installing Dependencies](#installing-dependencies)
* [Running the Automation](#running-the-automation)
* [Generating Test Reports](#generating-test-reports)
* [Test Flow](#test-flow)
* [Test Logging](#test-logging)
* [License](#license)

---

## Features

* Complete automation of the signup flow.
* Dynamic dropdown selection and hidden select handling.
* Handles checkboxes, text fields, and multi-step forms.
* PDF test report generation with log entries and colored statuses.
* Optional screenshots on errors.

---

## Prerequisites

* **Python 3.10+**
* **Google Chrome** installed
* **ChromeDriver** matching your Chrome version: [ChromeDriver](https://chromedriver.chromium.org/downloads)

---

## Setup

1. Clone this repository:

```bash
git clone <repository_url>
cd <repository_folder>
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

* **Windows:**

```bash
venv\Scripts\activate
```

* **macOS / Linux:**

```bash
source venv/bin/activate
```

---

## Installing Dependencies

1. Create a `requirements.txt` file with the following content:

```
selenium
reportlab
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Automation

1. Run the main automation script:

```bash
python signup_automation_script.py
```

2. You will be prompted to enter:

* Email address
* Phone number

3. Selenium will open Chrome and perform the signup steps automatically.

---

## Generating Test Reports

* The script automatically generates a **PDF report** (`test_report.pdf`) after execution.
* The report contains:

  * Test email
  * Test date and time
  * Overall status (SUCCESS / FAILED)
  * Execution log with timestamp and colored statuses
  * Screenshots on failure (if any)

---

## Test Flow

1. Navigate to login page.
2. Click **Sign Up**.
3. Check "Remember" checkbox.
4. Click **Continue**.
5. Fill personal details (First Name, Last Name, Email, Phone).
6. Set and confirm password.
7. Click **Next** and wait for verification.
8. Fill agency information (Agency Name, Role, Email, Website, Address).
9. Select country and region.
10. Fill professional experience:

    * Years of experience
    * Number of students recruited
    * Focus area
    * Success metrics
    * Services checkboxes
11. Fill business registration and preferred countries.
12. Select institution types and enter certification details.
13. Submit the form.
14. Generate PDF report with detailed logs.

---

## Running the Signup Automation

Run the signup automation script:

```bash
python signup_automation_script.py
The script will prompt you to enter:

Email for signup

Phone number for signup

Chrome browser will open automatically and complete the signup process.

Running Test Report Generation
After automation, you can generate a PDF test report using:

bash
Copy code
python py_test_signup_report.py
This will:

Run the signup automation with logging

Generate a PDF file named test_report.pdf

Include:

Execution log

Status (SUCCESS / FAILED)

Screenshots (if any failure occurs)

You will be prompted to enter:

Email for the test

Phone number for the test

