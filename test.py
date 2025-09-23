from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def generate_unique_email():
    """Generates a unique email using timestamp."""
    timestamp = int(time.time())
    return f"testuser_{timestamp}@example.com"


def init_driver():
    """Initializes and returns a Chrome WebDriver instance."""
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    return driver, wait


def navigate_to_signup(driver, wait):
    """Navigates from login page to signup form."""
    driver.get("https://authorized-partner.netlify.app/login")
    signup_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up")))
    signup_link.click()
    time.sleep(2)


def agree_to_terms(wait):
    """Clicks the checkbox to agree to terms and continues."""
    agree_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "remember")))
    agree_checkbox.click()
    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Continue']")))
    continue_button.click()
    time.sleep(2)


def fill_signup_form(driver, email="", password="", confirm_password="", phone_number=""):
    """Fills the signup form dynamically with provided data."""
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
    time.sleep(5)  # Allow any dynamic formatting to complete

    pwd_field = driver.find_element(By.NAME, "password")
    pwd_field.clear()
    pwd_field.send_keys(password)

    confirm_field = driver.find_element(By.NAME, "confirmPassword")
    confirm_field.clear()
    confirm_field.send_keys(confirm_password)


def submit_form(driver, wait):
    """Clicks the next button and waits for page response."""
    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next') or contains(text(),'Continue')]")))
    next_button.click()
    time.sleep(2)


def check_validation_error(driver):
    """Checks if validation error messages are displayed on the page."""
    errors = driver.find_elements(By.XPATH, "//p[contains(@class, 'text-red') or contains(text(),'required')]")
    if errors:
        print("Validation Errors Found:")
        for e in errors:
            print(f" - {e.text}")
        return True
    return False


def automate_signup():
    """Runs full signup flow with validation tests."""
    driver, wait = init_driver()
    email = generate_unique_email()
    password = "Test@12345"

    try:
        print(f"Starting Signup Test with email: {email}")
        navigate_to_signup(driver, wait)
        agree_to_terms(wait)

        # --- NEGATIVE TEST CASE 1: EMPTY FORM SUBMISSION ---
        print("Testing Empty Form Validation...")
        submit_form(driver, wait)
        if not check_validation_error(driver):
            print("Expected validation errors not displayed for empty form.")
        else:
            print("Empty form validation displayed as expected.")

        # --- NEGATIVE TEST CASE 2: PASSWORD MISMATCH ---
        print("Testing Password Mismatch Validation...")
        fill_signup_form(driver, email=email, password=password, confirm_password="WrongPass123", phone_number="9800000000")
        submit_form(driver, wait)
        if not check_validation_error(driver):
            print("xpected password mismatch error not displayed.")
        else:
            print("Password mismatch validation displayed as expected.")

        # --- POSITIVE TEST CASE: VALID SIGNUP ---
        print("Testing Valid Signup...")
        fill_signup_form(driver, email=email, password=password, confirm_password=password, phone_number="9800000000")
        submit_form(driver, wait)

        # Check for success or redirection
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'successfully') or contains(text(),'Welcome')]")))
            print("Signup completed successfully.")
        except:
            print("Signup did not complete as expected (check network/API).")
            driver.save_screenshot("signup_failed.png")

    except Exception as e:
        print(f"Test failed due to: {e}")
        driver.save_screenshot("unexpected_error.png")
    finally:
        time.sleep(3)
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    automate_signup()
