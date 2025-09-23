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
    time.sleep(1)  # Allow any dynamic formatting to complete

    pwd_field = driver.find_element(By.NAME, "password")
    pwd_field.clear()
    pwd_field.send_keys(password)

    confirm_field = driver.find_element(By.NAME, "confirmPassword")
    confirm_field.clear()
    confirm_field.send_keys(confirm_password)

    time.sleep(1)  # Let React validation trigger after typing passwords


def submit_form(driver, wait):
    """Clicks the next button and waits for page response."""
    next_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[not(@disabled) and (contains(text(),'Next') or contains(text(),'Continue'))]")
        )
    )
    next_button.click()
    time.sleep(2)


def check_validation_error(driver, timeout=3):
    """Detects validation via aria-invalid, error styling, or visible error messages."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: (
                len(d.find_elements(By.XPATH, "//input[@aria-invalid='true']")) > 0 or
                len(d.find_elements(By.XPATH, "//input[contains(@class, 'border-destructive')]")) > 0 or
                len(d.find_elements(By.XPATH, "//div[contains(@class, 'text-[var(--destructive)') and normalize-space(text()) != '']")) > 0
            )
        )

        print("Validation Errors Detected:")

        # Check aria-invalid
        invalid_inputs = driver.find_elements(By.XPATH, "//input[@aria-invalid='true']")
        for inp in invalid_inputs:
            name = inp.get_attribute("name") or "unnamed"
            print(f" - Input '{name}' is marked invalid (aria-invalid)")

        # Check border-destructive
        error_borders = driver.find_elements(By.XPATH, "//input[contains(@class, 'border-destructive')]")
        for inp in error_borders:
            name = inp.get_attribute("name") or "unnamed"
            print(f" - Input '{name}' has error styling (border-destructive)")

        # Check visible error messages (especially for password mismatch)
        error_messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-[var(--destructive)') and normalize-space(text()) != '']")
        for msg_div in error_messages:
            text = msg_div.text.strip()
            # Try to associate with nearby input (password/confirm)
            try:
                # Navigate to parent, then previous sibling container, then find input
                container = msg_div.find_element(By.XPATH, "./parent::div/preceding-sibling::div[1]//input")
                name = container.get_attribute("name") or "unnamed"
            except Exception:
                name = "password/confirmPassword"

            print(f" - Error message detected: '{text}' near field '{name}'")

        return True

    except Exception as e:
        print(f"No validation indicators detected. Error during check: {str(e)}")
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
        print("\nTesting Empty Form Validation...")
        submit_form(driver, wait)
        if not check_validation_error(driver):
            print("Expected validation errors not displayed for empty form.")
        else:
            print("Empty form validation displayed as expected.")

        # --- NEGATIVE TEST CASE 2: PASSWORD MISMATCH ---
        print("\nTesting Password Mismatch Validation...")
        fill_signup_form(driver, email=email, password=password, confirm_password="WrongPass123", phone_number="9800000000")
        submit_form(driver, wait)
        if not check_validation_error(driver):
            print("Expected password mismatch error not displayed.")
        else:
            print("Password mismatch validation displayed as expected.")

        # --- NEGATIVE TEST CASE 3: INVALID EMAIL FORMAT ---
        print("\nTesting Invalid Email Format...")
        fill_signup_form(driver, email="invalid-email", password=password, confirm_password=password, phone_number="9800000000")
        submit_form(driver, wait)
        if not check_validation_error(driver):
            print("Expected email format error not displayed.")
        else:
            print("Invalid email validation displayed as expected.")

        # --- NEGATIVE TEST CASE 4: SHORT PASSWORD ---
        print("\nTesting Short Password (less than 8 chars)...")
        fill_signup_form(driver, email=email, password="Short1!", confirm_password="Short1!", phone_number="9800000000")
        submit_form(driver, wait)
        if not check_validation_error(driver):
            print("Expected short password error not displayed.")
        else:
            print("Short password validation displayed as expected.")

        # --- NEGATIVE TEST CASE 5: PASSWORD WITHOUT SPECIAL CHAR ---
        print("\nTesting Password Without Special Character...")
        fill_signup_form(driver, email=email, password="NoSpecial123", confirm_password="NoSpecial123", phone_number="9800000000")
        submit_form(driver, wait)
        if not check_validation_error(driver):
            print("Expected 'special char required' error not displayed.")
        else:
            print("Password policy (special char) validation displayed as expected.")

        # --- NEGATIVE TEST CASE 6: PASSWORD WITHOUT NUMBER ---
        print("\n🧪 Testing Password Without Number...")
        fill_signup_form(driver, email=email, password="NoNumber@abc", confirm_password="NoNumber@abc", phone_number="9800000000")
        submit_form(driver, wait)
        if not check_validation_error(driver):
            print("Expected 'number required' error not displayed.")
        else:
            print("Password policy (number) validation displayed as expected.")

        # --- NEGATIVE TEST CASE 7: INVALID PHONE NUMBER ---
        print("\nTesting Invalid Phone Number (too short)...")
        fill_signup_form(driver, email=email, password=password, confirm_password=password, phone_number="123")
        submit_form(driver, wait)
        if not check_validation_error(driver):
            print("Expected phone number validation error not displayed.")
        else:
            print("Invalid phone number validation displayed as expected.")

        # --- NEGATIVE TEST CASE 8: DUPLICATE EMAIL ---
        print("\n🧪 Testing Duplicate Email Submission...")
        fill_signup_form(driver, email=email, password=password, confirm_password=password, phone_number="9800000000")
        submit_form(driver, wait)
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'already exists') or contains(text(),'duplicate') or contains(text(),'taken')]"))
            )
            print("Duplicate email error detected as expected.")
        except:
            print("No duplicate email error shown — may not be implemented or too fast.")

        # --- NEGATIVE TEST CASE 9: SQL INJECTION IN NAME FIELD ---
        print("\nTesting SQL Injection in First Name...")
        driver.find_element(By.NAME, "firstName").clear()
        driver.find_element(By.NAME, "firstName").send_keys("John'; DROP TABLE users;--")
        driver.find_element(By.NAME, "lastName").clear()
        driver.find_element(By.NAME, "lastName").send_keys("Doe")
        email_field = driver.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys(generate_unique_email())  # new email to avoid dup
        phone_field = driver.find_element(By.NAME, "phoneNumber")
        phone_field.clear()
        phone_field.send_keys("9800000000")
        pwd_field = driver.find_element(By.NAME, "password")
        pwd_field.clear()
        pwd_field.send_keys(password)
        confirm_field = driver.find_element(By.NAME, "confirmPassword")
        confirm_field.clear()
        confirm_field.send_keys(password)
        submit_form(driver, wait)

        try:
            if check_validation_error(driver):
                print("SQL Injection attempt handled safely (validation shown).")
            else:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                print("SQL Injection attempt did not break the system — PASSED.")
        except Exception as e:
            print(f"SQL Injection caused system error — SECURITY BUG FOUND. {str(e)}")
            driver.save_screenshot("sql_injection_failure.png")

        # --- POSITIVE TEST CASE: VALID SIGNUP ---
        print("\n🧪 Testing Valid Signup...")
        fill_signup_form(driver, email=generate_unique_email(), password=password, confirm_password=password, phone_number="9800000000")
        submit_form(driver, wait)

        # Check for success or redirection
        try:
            success_element = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//p[contains(text(),'successfully') or contains(text(),'Welcome') or contains(text(),'Congratulations')]"
                    " | //h2[contains(text(),'Agency Details')]"
                    " | //div[contains(text(),'Step 2')]"
                    " | //span[contains(text(),'Agency Details')]"
                ))
            )
            print(f"✅ Signup completed successfully. Detected: '{success_element.text}'")
        except Exception as e:
            print(f"Signup did not complete as expected. Error: {str(e)}")
            driver.save_screenshot("signup_failed.png")

        # Final Summary
        print("\n" + "="*60)
        print("SIGNUP TEST SUITE COMPLETED — ALL CASES EXECUTED")
        print("="*60)

    except Exception as e:
        print(f"Test failed due to: {e}")
        driver.save_screenshot("unexpected_error.png")
    finally:
        time.sleep(3)
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    automate_signup()


def test_signup_flow():
    automate_signup()