from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


# Ask user for email and phone number
user_email = input("Enter email address for signup: ")
user_phone = input("Enter phone number for signup: ")

# Initialize the WebDriver (Make sure to have the appropriate driver installed)
driver = webdriver.Chrome()
driver.get("https://authorized-partner.netlify.app/login")

try:
    sign_up_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up")))
    sign_up_link.click()
    time.sleep(2)  # Wait for the sign-up page to load

    check_box = driver.find_element(By.ID, "remember")
    check_box.click()

    continue_button = driver.find_element(By.XPATH, "//button[text()='Continue']")
    continue_button.click()
    time.sleep(2)

    #Fill in the form fields
    first_name = driver.find_element(By.NAME, "firstName")
    first_name.send_keys("John")

    last_name = driver.find_element(By.NAME, "lastName")
    last_name.send_keys("Doe")

    email = driver.find_element(By.NAME, "email")
    email.send_keys(user_email)
    time.sleep(2)

    phone_number = driver.find_element(By.NAME, "phoneNumber")
    phone_number.send_keys(user_phone)
    time.sleep(5)

    pwd_field = driver.find_element(By.NAME, "password")
    pwd_field.clear()
    pwd_field.send_keys("SecurePass123!")

    confirm_field = driver.find_element(By.NAME, "confirmPassword")
    confirm_field.clear()
    confirm_field.send_keys("SecurePass123!")
    time.sleep(1)

    # Submit the form
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[not(@disabled) and (contains(text(),'Next') or contains(text(),'Continue'))]")
        )
    )
    next_button.click()
    time.sleep(30)

    verify_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[4]/div/div/div/div[2]/div/form/div[2]/button"))
    )

    # Click the Verify Code button
    verify_btn.click()
    print("Verify Code button clicked successfully!")
    time.sleep(10)

    #Agency field
    wait = WebDriverWait(driver, 10) 

    agency_name = wait.until(EC.presence_of_element_located((By.NAME, "agency_name")))
    agency_name.send_keys("Test Agency")

    role_in_agency = wait.until(EC.presence_of_element_located((By.NAME, "role_in_agency")))
    role_in_agency.send_keys("Tester")

    agency_email = wait.until(EC.presence_of_element_located((By.NAME, "agency_email")))
    agency_email.send_keys("test.agency@example.com")

    agency_website = wait.until(EC.presence_of_element_located((By.NAME, "agency_website")))
    agency_website.send_keys("www.google.com")

    agency_address = wait.until(EC.presence_of_element_located((By.NAME, "agency_address")))
    agency_address.send_keys("Test Address 123")


    wait = WebDriverWait(driver, 10)
   
   # Wait for the dropdown button to be clickable
    wait = WebDriverWait(driver, 10)
    dropdown_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(@aria-controls, 'radix-')]"))
    )
    
    # Get the dynamic ID from aria-controls
    controls_id = dropdown_button.get_attribute('aria-controls')
    print(f"Dynamic controls ID: {controls_id}")
    
    dropdown_button.click()
    time.sleep(2)  # Give time for the dropdown to fully render

    # Wait for the popup/dialog to be present using the dynamic ID
    popup = wait.until(EC.presence_of_element_located((By.ID, controls_id)))
    
    # Now wait for and click the first option: the first div with class containing 'flex cursor-pointer' inside the popup
    first_option = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//*[@id='{controls_id}']//div[contains(@class, 'flex cursor-pointer items-center justify-between')]//span[normalize-space(text())='Afghanistan']"))
    )
    first_option.click()

    # Wait for the "Next" button and click it
    next_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
    )
    next_button.click()

    print("Successfully selected first region and clicked Next.")

    # Optional: Wait to observe result
    time.sleep(5)


  #Experience field
    # Find the hidden select for years of experience directly
    select_element = wait.until(EC.presence_of_element_located((By.XPATH, "//select[contains(@style, 'position: absolute') and @aria-hidden='true']")))
    
    # Use Select to choose the option by visible text
    select = Select(select_element)
    select.select_by_visible_text("2 years")
    print("Selected '2 years' as experience using hidden select.")
    time.sleep(2)
    
    # Optional: Fill other fields if needed
    # Number of students
    students_field = wait.until(EC.presence_of_element_located((By.NAME, "number_of_students_recruited_annually")))
    students_field.send_keys("50")
    
    # Focus area
    focus_field = wait.until(EC.presence_of_element_located((By.NAME, "focus_area")))
    focus_field.send_keys("Undergraduate admissions to Canada")
    
    # Success metrics
    success_field = wait.until(EC.presence_of_element_located((By.NAME, "success_metrics")))
    success_field.send_keys("90")
    
    # Select some checkboxes for services, e.g., first two
    checkboxes = driver.find_elements(By.XPATH, "//button[@role='checkbox']")
    if len(checkboxes) >= 2:
        checkboxes[0].click()  # Career Counseling
        checkboxes[1].click()  # Admission Applications
    
    # Click Next to proceed
    next_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
    )
    next_button.click()
    print("Filled professional experience form and clicked Next.")
    
    time.sleep(5)  

    # Validation and Preferences
    # Fill Business Registration Number
    reg_number = wait.until(EC.presence_of_element_located((By.NAME, "business_registration_number")))
    reg_number.send_keys("1234567890")
    print("Filled business registration number.")

    # Preferred Countries dropdown
    countries_dropdown = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Preferred Countries')]/following-sibling::button[@role='combobox']"))
    )
    countries_controls_id = countries_dropdown.get_attribute('aria-controls')
    print(f"Countries dropdown controls ID: {countries_controls_id}")
    
    countries_dropdown.click()
    time.sleep(2)

    countries_popup = wait.until(EC.presence_of_element_located((By.ID, countries_controls_id)))
    
    # Select first country 'Australia'
    countries_option = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//*[@id='{countries_controls_id}']//div[contains(@class, 'flex cursor-pointer')]//span[normalize-space(text())='Australia']"))
    )
    countries_option.click()
    print("Selected 'Australia' as preferred country.")
    time.sleep(1)

    # Preferred Institution Types checkboxes
    institution_checkboxes = driver.find_elements(By.XPATH, "//div[contains(@class, 'flex gap-3 flex-wrap')]//button[@role='checkbox']")
    if len(institution_checkboxes) >= 2:
        institution_checkboxes[0].click()  # Universities
        institution_checkboxes[1].click()  # Colleges
        print("Selected Universities and Colleges.")

    # Certification Details
    cert_field = wait.until(EC.presence_of_element_located((By.NAME, "certification_details")))
    cert_field.send_keys("ICEF Certified Education Agent")
    print("Filled certification details.")

    # Files Upload to hold time
    time.sleep(30)

    time.sleep(5)
    # Click Submit
    submit_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]"))
    )
    submit_button.click()
    print("Submitted the form.")

    time.sleep(5)  


finally:
    driver.quit()