from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
import os

# === CONFIGURATION ===
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SCREENSHOT_DIR = "test_screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# === HELPER FUNCTIONS ===

def generate_unique_email():
    """Generates a unique email using timestamp."""
    timestamp = int(time.time())
    return f"testuser_{timestamp}@example.com"

def init_driver(headless=False):
    """Initializes and returns a Chrome WebDriver instance."""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)  # Increased for reliability
    return driver, wait

def take_screenshot(driver, name):
    """Takes screenshot and saves to folder."""
    timestamp = int(time.time())
    path = os.path.join(SCREENSHOT_DIR, f"{name}_{timestamp}.png")
    driver.save_screenshot(path)
    logger.info(f"Screenshot saved: {path}")
    return path

def debug_form_state(driver):
    """Logs current state of all key form fields for debugging."""
    logger.debug("=== FORM STATE DEBUG ===")
    fields = {
        "firstName": "//input[@name='firstName']",
        "lastName": "//input[@name='lastName']",
        "email": "//input[@name='email']",
        "phoneNumber": "//input[@name='phoneNumber']",
        "password": "//input[@name='password']",
        "confirmPassword": "//input[@name='confirmPassword']"
    }
    
    for name, xpath in fields.items():
        try:
            el = driver.find_element(By.XPATH, xpath)
            value = el.get_attribute("value") or "(empty)"
            aria_invalid = el.get_attribute("aria-invalid")
            classes = el.get_attribute("class") or ""
            is_error_border = "border-destructive" in classes
            logger.debug(f"{name}: value='{value}', aria-invalid={aria_invalid}, has_error_border={is_error_border}")
        except:
            logger.debug(f"{name}: NOT FOUND")
    logger.debug("=== END FORM STATE ===")

def wait_for_validation_appear(driver, timeout=5):
    """Waits for any validation indicator to appear after interaction."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: (
                len(d.find_elements(By.XPATH, "//input[@aria-invalid='true']")) > 0 or
                len(d.find_elements(By.XPATH, "//input[contains(@class, 'border-destructive')]")) > 0 or
                len(d.find_elements(By.XPATH, "//*[contains(@class, 'text-destructive') or contains(text(), 'error') or contains(text(), 'required')]")) > 0
            )
        )
        return True
    except TimeoutException:
        return False

def check_validation_error(driver, scenario=""):
    """
    Comprehensive validation detector.
    Returns dict: {found: bool, details: list}
    """
    details = []
    found = False

    # 1. Check ARIA-invalid
    invalid_inputs = driver.find_elements(By.XPATH, "//input[@aria-invalid='true']")
    for inp in invalid_inputs:
        name = inp.get_attribute("name") or "unnamed"
        details.append(f"ARIA-invalid on '{name}'")
        found = True

    # 2. Check error styling
    error_borders = driver.find_elements(By.XPATH, "//input[contains(@class, 'border-destructive')]")
    for inp in error_borders:
        name = inp.get_attribute("name") or "unnamed"
        if f"ARIA-invalid on '{name}'" not in details:
            details.append(f"Error border on '{name}'")
            found = True

    # 3. Check visible error messages
    error_texts = driver.find_elements(By.XPATH, 
        "//*[contains(@class, 'text-destructive') or contains(@class, 'text-[var(--destructive)]')] | "
        "//*[contains(text(), 'required') or contains(text(), 'match') or contains(text(), 'invalid') or contains(text(), 'at least')]"
    )
    for el in error_texts:
        txt = el.text.strip()
        if txt and txt not in details:
            details.append(f"Error msg: '{txt}'")
            found = True

    if found:
        logger.info(f"✅ Validation detected [{scenario}]:")
        for d in details:
            logger.info(f"   • {d}")
    else:
        logger.warning(f"❌ No validation detected [{scenario}]")

    return {"found": found, "details": details}

def check_password_mismatch(driver):
    """Specifically checks if password & confirm are invalid while others are valid."""
    try:
        pwd = driver.find_element(By.NAME, "password")
        confirm = driver.find_element(By.NAME, "confirmPassword")
        
        pwd_invalid = pwd.get_attribute("aria-invalid") == "true"
        confirm_invalid = confirm.get_attribute("aria-invalid") == "true"
        
        # Check if other fields are valid (to confirm it's mismatch, not general invalid)
        other_fields = ["firstName", "lastName", "email", "phoneNumber"]
        other_invalid = False
        for field_name in other_fields:
            try:
                el = driver.find_element(By.NAME, field_name)
                if el.get_attribute("aria-invalid") == "true":
                    other_invalid = True
                    break
            except:
                continue

        if pwd_invalid and confirm_invalid and not other_invalid:
            logger.info("✅ Password mismatch correctly isolated")
            return True
        elif pwd_invalid and confirm_invalid:
            logger.info("⚠️  Password fields invalid but other fields also invalid")
            return True  # Still consider it detected
        return False
    except Exception as e:
        logger.error(f"Error checking password mismatch: {e}")
        return False

# === PAGE OBJECT METHODS ===

def navigate_to_signup(driver, wait):
    """Navigates from login page to signup form."""
    logger.info("Navigating to signup page...")
    driver.get("https://authorized-partner.netlify.app/login")
    try:
        signup_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up")))
        signup_link.click()
        time.sleep(2)
        logger.info("✅ Navigated to signup form")
    except Exception as e:
        take_screenshot(driver, "navigate_signup_failed")
        raise Exception(f"Failed to navigate to signup: {e}")

def agree_to_terms(wait):
    """Clicks the checkbox to agree to terms and continues."""
    logger.info("Agreeing to terms...")
    try:
        agree_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "remember")))
        agree_checkbox.click()
        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Continue']")))
        continue_button.click()
        time.sleep(2)
        logger.info("✅ Agreed to terms and continued")
    except Exception as e:
        take_screenshot(driver, "agree_terms_failed")
        raise Exception(f"Failed to agree to terms: {e}")

def fill_signup_form(driver, firstName="John", lastName="Doe", email="", password="", confirm_password="", phone_number=""):
    """Fills the signup form dynamically with provided data."""
    logger.info("Filling signup form...")
    try:
        # Clear and fill each field
        fields = [
            ("firstName", firstName),
            ("lastName", lastName),
            ("email", email),
            ("phoneNumber", phone_number),
            ("password", password),
            ("confirmPassword", confirm_password)
        ]
        
        for name, value in fields:
            field = driver.find_element(By.NAME, name)
            field.clear()
            if value:
                field.send_keys(value)
            logger.debug(f"Filled {name}: {value if value else '(empty)'}")
        
        # Wait for any dynamic formatting (phone, etc.)
        time.sleep(2)
        logger.info("✅ Form filled successfully")
    except Exception as e:
        take_screenshot(driver, "fill_form_failed")
        raise Exception(f"Failed to fill form: {e}")

def submit_form(driver, wait):
    """Clicks the next button and waits for response."""
    logger.info("Submitting form...")
    try:
        next_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Next') or contains(text(),'Continue')]")))
        next_button.click()
        time.sleep(1)  # Short wait before checking validation
        logger.info("✅ Form submitted")
    except Exception as e:
        take_screenshot(driver, "submit_form_failed")
        raise Exception(f"Failed to submit form: {e}")

def check_successful_navigation(driver, wait):
    """Checks if signup completed successfully via navigation or success message."""
    logger.info("Checking for successful signup...")
    try:
        WebDriverWait(driver, 10).until(
            lambda d: (
                "dashboard" in d.current_url.lower() or
                "welcome" in d.current_url.lower() or
                len(d.find_elements(By.XPATH, "//*[contains(text(), 'success') or contains(text(), 'welcome') or contains(text(), 'dashboard') or contains(text(), 'complete')]")) > 0
            )
        )
        logger.info(f"✅ Signup successful! Current URL: {driver.current_url}")
        return True
    except TimeoutException:
        logger.error(f"❌ Signup failed - still on: {driver.current_url}")
        take_screenshot(driver, "signup_failed")
        return False

# === TEST CASES ===

class TestResults:
    def __init__(self):
        self.results = []
    
    def add_result(self, test_name, passed, details=""):
        result = {
            "test_name": test_name,
            "passed": passed,
            "details": details,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.results.append(result)
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{status} {test_name} - {details}")
    
    def print_summary(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        failed = total - passed
        
        logger.info("\n" + "="*50)
        logger.info("TEST EXECUTION SUMMARY")
        logger.info("="*50)
        for result in self.results:
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            logger.info(f"{status} {result['test_name']}")
        logger.info("="*50)
        logger.info(f"Total: {total} | Passed: {passed} | Failed: {failed}")
        logger.info("="*50)
        
        if failed > 0:
            logger.error("❌ SOME TESTS FAILED!")
        else:
            logger.info("🎉 ALL TESTS PASSED!")

# === MAIN TEST ORCHESTRATOR ===

def automate_signup():
    """Runs full signup flow with comprehensive validation tests."""
    driver, wait = init_driver()
    test_results = TestResults()
    email = generate_unique_email()
    password = "Test@12345"
    
    logger.info(f"🚀 Starting Signup Test Suite with email: {email}")

    try:
        # Navigate and agree to terms
        navigate_to_signup(driver, wait)
        agree_to_terms(wait)

        # === TEST CASE 1: EMPTY FORM VALIDATION ===
        logger.info("\n=== TEST CASE 1: EMPTY FORM VALIDATION ===")
        fill_signup_form(driver, email="", password="", confirm_password="", phone_number="")
        submit_form(driver, wait)
        
        # Wait for validation to appear (async)
        if wait_for_validation_appear(driver, 5):
            validation = check_validation_error(driver, "Empty Form")
            if validation["found"]:
                test_results.add_result("Empty Form Validation", True, "Validation errors detected as expected")
            else:
                test_results.add_result("Empty Form Validation", False, "No validation errors detected")
                take_screenshot(driver, "empty_form_no_validation")
                debug_form_state(driver)
        else:
            test_results.add_result("Empty Form Validation", False, "Validation did not appear within timeout")
            take_screenshot(driver, "empty_form_timeout")
            debug_form_state(driver)

        # === TEST CASE 2: PASSWORD MISMATCH VALIDATION ===
        logger.info("\n=== TEST CASE 2: PASSWORD MISMATCH VALIDATION ===")
        fill_signup_form(driver, email=email, password=password, confirm_password="WrongPass123", phone_number="9800000000")
        submit_form(driver, wait)
        
        if wait_for_validation_appear(driver, 5):
            if check_password_mismatch(driver):
                test_results.add_result("Password Mismatch Validation", True, "Password mismatch correctly detected")
            else:
                validation = check_validation_error(driver, "Password Mismatch")
                if validation["found"]:
                    test_results.add_result("Password Mismatch Validation", True, "General validation detected")
                else:
                    test_results.add_result("Password Mismatch Validation", False, "No validation detected for mismatch")
                    take_screenshot(driver, "password_mismatch_no_validation")
                    debug_form_state(driver)
        else:
            test_results.add_result("Password Mismatch Validation", False, "Validation did not appear within timeout")
            take_screenshot(driver, "password_mismatch_timeout")
            debug_form_state(driver)

        # === TEST CASE 3: INVALID EMAIL FORMAT ===
        logger.info("\n=== TEST CASE 3: INVALID EMAIL FORMAT ===")
        fill_signup_form(driver, email="invalid-email", password=password, confirm_password=password, phone_number="9800000000")
        submit_form(driver, wait)
        
        if wait_for_validation_appear(driver, 5):
            validation = check_validation_error(driver, "Invalid Email")
            email_invalid = any("email" in detail for detail in validation["details"]) if validation["found"] else False
            if email_invalid:
                test_results.add_result("Invalid Email Validation", True, "Email validation detected")
            else:
                test_results.add_result("Invalid Email Validation", False, "Email field not marked invalid")
                take_screenshot(driver, "invalid_email_no_validation")
        else:
            test_results.add_result("Invalid Email Validation", False, "Validation did not appear within timeout")
            take_screenshot(driver, "invalid_email_timeout")

        # === TEST CASE 4: WEAK PASSWORD ===
        logger.info("\n=== TEST CASE 4: WEAK PASSWORD VALIDATION ===")
        fill_signup_form(driver, email=email, password="weak", confirm_password="weak", phone_number="9800000000")
        submit_form(driver, wait)
        
        if wait_for_validation_appear(driver, 5):
            validation = check_validation_error(driver, "Weak Password")
            password_invalid = any("password" in detail for detail in validation["details"]) if validation["found"] else False
            if password_invalid:
                test_results.add_result("Weak Password Validation", True, "Password strength validation detected")
            else:
                test_results.add_result("Weak Password Validation", False, "Password field not marked invalid")
                take_screenshot(driver, "weak_password_no_validation")
        else:
            test_results.add_result("Weak Password Validation", False, "Validation did not appear within timeout")
            take_screenshot(driver, "weak_password_timeout")

        # === TEST CASE 5: VALID SIGNUP ===
        logger.info("\n=== TEST CASE 5: VALID SIGNUP ===")
        fill_signup_form(driver, email=email, password=password, confirm_password=password, phone_number="9800000000")
        submit_form(driver, wait)
        
        if check_successful_navigation(driver, wait):
            test_results.add_result("Valid Signup", True, "User successfully signed up")
        else:
            test_results.add_result("Valid Signup", False, "Signup did not complete successfully")
            debug_form_state(driver)

    except Exception as e:
        logger.error(f"❌ Test execution failed due to: {e}")
        take_screenshot(driver, "unexpected_error")
        test_results.add_result("Test Execution", False, f"Unexpected error: {e}")
    finally:
        time.sleep(3)
        driver.quit()
        logger.info("🏁 Browser closed.")
        test_results.print_summary()
        return test_results

# === ENTRY POINT ===

if __name__ == "__main__":
    results = automate_signup()
    
    # Exit with non-zero code if any tests failed (for CI/CD)
    failed_tests = sum(1 for r in results.results if not r["passed"])
    if failed_tests > 0:
        exit(1)
    else:
        exit(0)