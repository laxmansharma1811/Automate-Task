from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import time
import datetime
import os

# Global list to collect log entries
test_log = []

def log_step(message, status="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{status}] {message}"
    test_log.append(entry)
    print(entry)

def generate_pdf_report(email, success=True):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"signup_report_{timestamp}.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=14,
        textColor='darkblue'
    )
    story.append(Paragraph("Signup Automation Test Report", title_style))
    story.append(Spacer(1, 12))

    # Metadata
    meta_style = styles["Normal"]
    story.append(Paragraph(f"<b>Test Email:</b> {email}", meta_style))
    story.append(Paragraph(f"<b>Test Date:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", meta_style))
    story.append(Paragraph(f"<b>Status:</b> {'✅ SUCCESS' if success else '❌ FAILED'}", meta_style))
    story.append(Spacer(1, 12))

    # Log entries
    story.append(Paragraph("Execution Log:", styles['Heading2']))
    for entry in test_log:
        # Color-code based on status
        if "[ERROR]" in entry:
            story.append(Paragraph(entry, ParagraphStyle('Error', parent=styles['Normal'], textColor='red')))
        elif "[SUCCESS]" in entry or "✅" in entry:
            story.append(Paragraph(entry, ParagraphStyle('Success', parent=styles['Normal'], textColor='green')))
        else:
            story.append(Paragraph(entry, styles['Normal']))
        story.append(Spacer(1, 4))

    doc.build(story)
    log_step(f"PDF report saved as: {filename}", "INFO")

def run_signup_flow(user_email, user_phone):
    """Runs the complete signup automation flow with PDF reporting."""
    driver = None
    success = False
    try:
        driver = webdriver.Chrome()
        driver.get("https://authorized-partner.netlify.app/login")

        log_step("Navigated to login page.")

        sign_up_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up"))
        )
        sign_up_link.click()
        time.sleep(2)
        log_step("Clicked 'Sign Up' link.")

        check_box = driver.find_element(By.ID, "remember")
        check_box.click()
        log_step("Checked 'Remember' checkbox.")

        continue_button = driver.find_element(By.XPATH, "//button[text()='Continue']")
        continue_button.click()
        time.sleep(2)
        log_step("Clicked 'Continue' button.")

        # Fill personal info
        driver.find_element(By.NAME, "firstName").send_keys("John")
        driver.find_element(By.NAME, "lastName").send_keys("Doe")
        driver.find_element(By.NAME, "email").send_keys(user_email)
        driver.find_element(By.NAME, "phoneNumber").send_keys(user_phone)
        log_step("Filled personal information.")

        # Set password
        pwd = "SecurePass123!"
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys(pwd)
        driver.find_element(By.NAME, "confirmPassword").clear()
        driver.find_element(By.NAME, "confirmPassword").send_keys(pwd)
        log_step("Set and confirmed password.")

        # Click Next
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[not(@disabled) and (contains(text(),'Next') or contains(text(),'Continue'))]"))
        )
        next_button.click()
        time.sleep(30)
        log_step("Clicked 'Next' after password setup.")

        # Click Verify Code
        verify_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[4]/div/div/div/div[2]/div/form/div[2]/button"))
        )
        verify_btn.click()
        log_step("✅ Verify Code button clicked successfully!")

        # Fill agency info
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "agency_name"))).send_keys("Test Agency")
        wait.until(EC.presence_of_element_located((By.NAME, "role_in_agency"))).send_keys("Tester")
        wait.until(EC.presence_of_element_located((By.NAME, "agency_email"))).send_keys("test.agency@example.com")
        wait.until(EC.presence_of_element_located((By.NAME, "agency_website"))).send_keys("www.google.com")
        wait.until(EC.presence_of_element_located((By.NAME, "agency_address"))).send_keys("Test Address 123")
        log_step("Filled agency information.")

        # Select country
        dropdown_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(@aria-controls, 'radix-')]"))
        )
        controls_id = dropdown_button.get_attribute('aria-controls')
        dropdown_button.click()
        time.sleep(2)
        first_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//*[@id='{controls_id}']//span[normalize-space(text())='Afghanistan']"))
        )
        first_option.click()
        log_step("Selected country: Afghanistan.")

        # Click Next
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]")))
        next_button.click()
        log_step("✅ Successfully selected region and clicked Next.")

        # Select experience
        select_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//select[@aria-hidden='true']"))
        )
        Select(select_element).select_by_visible_text("2 years")
        log_step("✅ Selected '2 years' experience.")

        # Fill professional info
        wait.until(EC.presence_of_element_located((By.NAME, "number_of_students_recruited_annually"))).send_keys("50")
        wait.until(EC.presence_of_element_located((By.NAME, "focus_area"))).send_keys("Undergraduate admissions to Canada")
        wait.until(EC.presence_of_element_located((By.NAME, "success_metrics"))).send_keys("90")

        # Check checkboxes
        checkboxes = driver.find_elements(By.XPATH, "//button[@role='checkbox']")
        if len(checkboxes) >= 2:
            checkboxes[0].click()
            checkboxes[1].click()
        log_step("Selected service types.")

        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]")))
        next_button.click()
        log_step("✅ Filled professional experience and clicked Next.")

        # Final form
        wait.until(EC.presence_of_element_located((By.NAME, "business_registration_number"))).send_keys("1234567890")
        log_step("✅ Filled business registration number.")

        # Preferred country
        countries_dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Preferred Countries')]/following-sibling::button[@role='combobox']"))
        )
        countries_controls_id = countries_dropdown.get_attribute('aria-controls')
        countries_dropdown.click()
        time.sleep(2)
        countries_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//*[@id='{countries_controls_id}']//span[normalize-space(text())='Australia']"))
        )
        countries_option.click()
        log_step("✅ Selected 'Australia' as preferred country.")

        # Institution types
        institution_checkboxes = driver.find_elements(By.XPATH, "//button[@role='checkbox']")
        if len(institution_checkboxes) >= 2:
            institution_checkboxes[0].click()
            institution_checkboxes[1].click()
        log_step("✅ Selected Universities and Colleges.")

        # Certification
        wait.until(EC.presence_of_element_located((By.NAME, "certification_details"))).send_keys("ICEF Certified Education Agent")
        log_step("✅ Filled certification details.")

        time.sleep(30)  # Wait for manual OTP or auto-fill

        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]")))
        submit_button.click()
        log_step("✅ Submitted the form.")
        success = True

    except Exception as e:
        log_step(f"❌ Test failed with error: {str(e)}", "ERROR")
        success = False
        # Optional: take screenshot
        if driver:
            screenshot_name = f"error_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(screenshot_name)
            log_step(f"Screenshot saved: {screenshot_name}", "INFO")
    finally:
        if driver:
            driver.quit()
        generate_pdf_report(user_email, success=success)

def main():
    user_email = input("Enter email address for signup: ").strip()
    user_phone = input("Enter phone number for signup: ").strip()
    if not user_email or not user_phone:
        print("Email and phone are required.")
        return
    run_signup_flow(user_email, user_phone)

if __name__ == "__main__":
    main()