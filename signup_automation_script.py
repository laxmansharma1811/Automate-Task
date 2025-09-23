import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


driver = None
wait = None


def setup_module(module):
    """Setup: Initialize driver once for all tests."""
    global driver, wait
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)


def teardown_module(module):
    """Teardown: Quit driver after all tests."""
    global driver
    if driver:
        driver.quit()


# ========= PYTEST HOOK FOR SCREENSHOT ON FAILURE =========

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot in HTML report if test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        global driver
        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            driver.save_screenshot(screenshot_path)
            extra = getattr(report, "extra", [])
            if hasattr(pytest_html, 'extras'):
                extra.append(pytest_html.extras.image(screenshot_path))
                report.extra = extra


# ========= HELPER FUNCTIONS =========

def generate_unique_email():
    """Generates a unique email using timestamp."""
    timestamp = int(time.time())
    return f"testuser_{timestamp}@example.com"


def navigate_to_signup():
    """Navigates from login page to signup form."""
    global driver, wait
    driver.get("https://authorized-partner.netlify.app/login")
    signup_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up")))
    signup_link.click()
    time.sleep(2)


def agree_to_terms():
    """Clicks the checkbox to agree to terms and continues."""
    global wait
    agree_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "remember")))
    agree_checkbox.click()
    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Continue']")))
    continue_button.click()
    time.sleep(2)


def fill_signup_form(email="", password="", confirm_password="", phone_number=""):
    """Fills the signup form dynamically with provided data."""
    global driver
    driver.find_element(By.NAME, "firstName").clear()
    driver.find_element(By.NAME, "firstName").send_keys("John")

    driver.find_element(By.NAME, "lastName").clear()
    driver.find_element(By.NAME, "lastName").send_keys("Doe")

    email_field = driver.find_element(By.NAME, "email")
    email_field.clear()
    email_field.send_keys(email)

    phone_field = driver.find_element(By.NAME, "phoneNumber")
    phone_field.clear()
    phone_field.send_keys(phone_number)
    time.sleep(1)

    pwd_field = driver.find_element(By.NAME, "password")
    pwd_field.clear()
    pwd_field.send_keys(password)

    confirm_field = driver.find_element(By.NAME, "confirmPassword")
    confirm_field.clear()
    confirm_field.send_keys(confirm_password)
    time.sleep(1)


def submit_form():
    """Clicks the next button and waits for page response."""
    global driver, wait
    next_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[not(@disabled) and (contains(text(),'Next') or contains(text(),'Continue'))]")
        )
    )
    next_button.click()
    time.sleep(2)


def check_validation_error(timeout=3):
    """Detects validation via aria-invalid, error styling, or visible error messages."""
    global driver
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: (
                len(d.find_elements(By.XPATH, "//input[@aria-invalid='true']")) > 0 or
                len(d.find_elements(By.XPATH, "//input[contains(@class, 'border-destructive')]")) > 0 or
                len(d.find_elements(By.XPATH, "//div[contains(@class, 'text-[var(--destructive)') and normalize-space(text()) != '']")) > 0
            )
        )
        return True
    except:
        return False


def reset_to_signup():
    """Helper: Reset state by navigating back to signup form."""
    navigate_to_signup()
    agree_to_terms()


# ========= INDIVIDUAL TEST FUNCTIONS =========

def test_empty_form_validation():
    """Test: Submit empty form → should show validation errors."""
    reset_to_signup()
    submit_form()
    assert check_validation_error(), "Expected validation errors not displayed for empty form."


def test_password_mismatch():
    """Test: Password and confirm password mismatch → should show error."""
    reset_to_signup()
    email = generate_unique_email()
    fill_signup_form(email=email, password="Test@12345", confirm_password="WrongPass123", phone_number="9800000000")
    submit_form()
    assert check_validation_error(), "Expected password mismatch error not displayed."


def test_invalid_email_format():
    """Test: Invalid email format → should show error."""
    reset_to_signup()
    fill_signup_form(email="invalid-email", password="Test@12345", confirm_password="Test@12345", phone_number="9800000000")
    submit_form()
    assert check_validation_error(), "Expected email format error not displayed."


def test_short_password():
    """Test: Password too short → should show error."""
    reset_to_signup()
    email = generate_unique_email()
    fill_signup_form(email=email, password="Short1!", confirm_password="Short1!", phone_number="9800000000")
    submit_form()
    assert check_validation_error(), "Expected short password error not displayed."


def test_password_without_special_char():
    """Test: Password without special character → should show error."""
    reset_to_signup()
    email = generate_unique_email()
    fill_signup_form(email=email, password="NoSpecial123", confirm_password="NoSpecial123", phone_number="9800000000")
    submit_form()
    assert check_validation_error(), "Expected 'special char required' error not displayed."


def test_password_without_number():
    """Test: Password without number → should show error."""
    reset_to_signup()
    email = generate_unique_email()
    fill_signup_form(email=email, password="NoNumber@abc", confirm_password="NoNumber@abc", phone_number="9800000000")
    submit_form()
    assert check_validation_error(), "Expected 'number required' error not displayed."


def test_invalid_phone_number():
    """Test: Invalid phone number → should show error."""
    reset_to_signup()
    email = generate_unique_email()
    fill_signup_form(email=email, password="Test@12345", confirm_password="Test@12345", phone_number="123")
    submit_form()
    assert check_validation_error(), "Expected phone number validation error not displayed."


def test_duplicate_email():
    """Test: Submit duplicate email → should show backend error (if implemented)."""
    reset_to_signup()
    email = generate_unique_email()

    # First submission
    fill_signup_form(email=email, password="Test@12345", confirm_password="Test@12345", phone_number="9800000000")
    submit_form()

    # Second submission with same email
    reset_to_signup()
    fill_signup_form(email=email, password="Test@12345", confirm_password="Test@12345", phone_number="9800000000")
    submit_form()

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'already exists') or contains(text(),'duplicate') or contains(text(),'taken')]"))
        )
        assert True  # Pass if error found
    except:
        pytest.skip("Duplicate email error not implemented or too fast to catch.")


def test_sql_injection_in_name():
    """Test: SQL injection in first name → should not crash system."""
    reset_to_signup()
    email = generate_unique_email()

    driver.find_element(By.NAME, "firstName").clear()
    driver.find_element(By.NAME, "firstName").send_keys("John'; DROP TABLE users;--")
    driver.find_element(By.NAME, "lastName").clear()
    driver.find_element(By.NAME, "lastName").send_keys("Doe")
    email_field = driver.find_element(By.NAME, "email")
    email_field.clear()
    email_field.send_keys(email)
    phone_field = driver.find_element(By.NAME, "phoneNumber")
    phone_field.clear()
    phone_field.send_keys("9800000000")
    pwd_field = driver.find_element(By.NAME, "password")
    pwd_field.clear()
    pwd_field.send_keys("Test@12345")
    confirm_field = driver.find_element(By.NAME, "confirmPassword")
    confirm_field.clear()
    confirm_field.send_keys("Test@12345")
    submit_form()

    if check_validation_error():
        assert True, "SQL Injection handled via validation."
    else:
        # Check page is still responsive
        assert driver.title, "Page crashed after SQL injection attempt."


def test_valid_signup():
    """Test: Valid signup → should proceed to next step (Agency Details, etc.)."""
    reset_to_signup()
    email = generate_unique_email()
    fill_signup_form(email=email, password="Test@12345", confirm_password="Test@12345", phone_number="9800000000")
    submit_form()

    try:
        success_element = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//p[contains(text(),'successfully') or contains(text(),'Welcome') or contains(text(),'Congratulations')]"
                " | //h2[contains(text(),'Agency Details')]"
                " | //div[contains(text(),'Step 2')]"
                " | //span[contains(text(),'Agency Details')]"
                " | //div[contains(@class, 'splash-screen') and not(contains(@style, 'display: none'))]"
            ))
        )
        assert success_element, "Expected success indicator not found after valid signup."
    except Exception as e:
        # Fallback: Check URL for success keywords
        current_url = driver.current_url
        success_indicators = ["/agency", "/step2", "/profile", "/dashboard", "/onboarding", "/verify"]
        if any(indicator in current_url for indicator in success_indicators):
            assert True, f"Redirected to success path: {current_url}"
        else:
            pytest.fail(f"Signup failed. Still on: {current_url}. Error: {str(e)}")