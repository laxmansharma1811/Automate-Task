from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


def run_signup_flow(user_email, user_phone):
    """Runs the complete signup automation flow."""
    driver = webdriver.Chrome()
    driver.get("https://authorized-partner.netlify.app/login")

    try:
        sign_up_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up"))
        )
        sign_up_link.click()
        time.sleep(2)

        check_box = driver.find_element(By.ID, "remember")
        check_box.click()

        continue_button = driver.find_element(By.XPATH, "//button[text()='Continue']")
        continue_button.click()
        time.sleep(2)

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
        verify_btn.click()
        print("Verify Code button clicked successfully!")
        time.sleep(10)

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

        dropdown_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(@aria-controls, 'radix-')]"))
        )
        controls_id = dropdown_button.get_attribute('aria-controls')
        print(f"Dynamic controls ID: {controls_id}")

        dropdown_button.click()
        time.sleep(2)

        popup = wait.until(EC.presence_of_element_located((By.ID, controls_id)))
        first_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//*[@id='{controls_id}']//div[contains(@class, 'flex cursor-pointer items-center justify-between')]//span[normalize-space(text())='Afghanistan']")
            )
        )
        first_option.click()

        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
        )
        next_button.click()
        print("Successfully selected first region and clicked Next.")
        time.sleep(5)

        select_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@style, 'position: absolute') and @aria-hidden='true']"))
        )
        select = Select(select_element)
        select.select_by_visible_text("2 years")
        print("Selected '2 years' as experience using hidden select.")
        time.sleep(2)

        students_field = wait.until(EC.presence_of_element_located((By.NAME, "number_of_students_recruited_annually")))
        students_field.send_keys("50")

        focus_field = wait.until(EC.presence_of_element_located((By.NAME, "focus_area")))
        focus_field.send_keys("Undergraduate admissions to Canada")

        success_field = wait.until(EC.presence_of_element_located((By.NAME, "success_metrics")))
        success_field.send_keys("90")

        checkboxes = driver.find_elements(By.XPATH, "//button[@role='checkbox']")
        if len(checkboxes) >= 2:
            checkboxes[0].click()
            checkboxes[1].click()

        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
        )
        next_button.click()
        print("Filled professional experience form and clicked Next.")
        time.sleep(5)

        reg_number = wait.until(EC.presence_of_element_located((By.NAME, "business_registration_number")))
        reg_number.send_keys("1234567890")
        print("Filled business registration number.")

        countries_dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Preferred Countries')]/following-sibling::button[@role='combobox']"))
        )
        countries_controls_id = countries_dropdown.get_attribute('aria-controls')
        print(f"Countries dropdown controls ID: {countries_controls_id}")

        countries_dropdown.click()
        time.sleep(2)

        countries_popup = wait.until(EC.presence_of_element_located((By.ID, countries_controls_id)))
        countries_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//*[@id='{countries_controls_id}']//div[contains(@class, 'flex cursor-pointer')]//span[normalize-space(text())='Australia']")
            )
        )
        countries_option.click()
        print("Selected 'Australia' as preferred country.")
        time.sleep(1)

        institution_checkboxes = driver.find_elements(By.XPATH, "//div[contains(@class, 'flex gap-3 flex-wrap')]//button[@role='checkbox']")
        if len(institution_checkboxes) >= 2:
            institution_checkboxes[0].click()
            institution_checkboxes[1].click()
            print("Selected Universities and Colleges.")

        cert_field = wait.until(EC.presence_of_element_located((By.NAME, "certification_details")))
        cert_field.send_keys("ICEF Certified Education Agent")
        print("Filled certification details.")

        time.sleep(30)
        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]"))
        )
        submit_button.click()
        print("Submitted the form.")
        time.sleep(5)

    finally:
        driver.quit()


def main():
    user_email = input("Enter email address for signup: ")
    user_phone = input("Enter phone number for signup: ")
    run_signup_flow(user_email, user_phone)


if __name__ == "__main__":
    main()
