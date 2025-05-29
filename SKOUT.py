# === IMPORTS ===
from dotenv import load_dotenv
import time  # For sleep delays between actions
import sys, os   # (Unused) Could be used for handling script arguments or exiting

# Selenium imports for browser automation
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


load_dotenv()  # Load variables from .env

# === LOGGING SETUP ===
log_file_path = "profiles1.txt"

# Simple logger that prints messages and appends them to a file
def log(message):
    print(message)
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(message + "\n")

# === SELENIUM CONFIGURATION ===

# Define paths to the ChromeDriver binary, Chrome executable, and user data profile directory
#chrome_driver_path = r"C:\Users\DEREK\PythonScripts\SKOUT\chromedriver.exe"
#chrome_binary_path = r"C:\Users\DEREK\Downloads\chrometesting136\chrome-win64\chrome.exe"
#user_data_dir = r"C:\Users\DEREK\PythonScripts\SKOUT\chrome_user_data"

chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
chrome_binary_path = os.getenv("CHROME_BINARY_PATH")
user_data_dir = os.getenv("USER_DATA_DIR")

# Set Chrome options
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")  # Helps avoid bot detection
options.add_argument("--start-maximized")  # Launch Chrome in full-screen
options.add_argument(f"user-data-dir={user_data_dir}")  # Use a persistent browser profile for session storage (cookies, logins, etc.)

# === INITIALIZE THE BROWSER ===
# Start Chrome browser with specified options and driver path
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

# Navigate to Skout website
driver.get("https://skout.com")

# === OPTIONAL LOGIN HANDLING ===
# If the session is not preserved, try to locate and click the login button
try:
    login_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-login-navigation"]/li/a'))
    )
    login_button.click()
    log("🔐 Clicked the login button.")
except:
    log("⚠️ Login button not found or already logged in.")  # If already logged in, this will likely throw and be ignored

# Wait for page to fully load by checking the readyState
log("⏳ Waiting for the page to load...")
WebDriverWait(driver, 5).until(lambda d: d.execute_script('return document.readyState') == 'complete')
log("✅ Page loaded successfully!")

# === TRACKING PROFILES TO AVOID DUPLICATES ===
seen_profiles = set()  # Set to track profile keys (name + suburb) and avoid duplicates

# === PAGE SCROLL FUNCTION ===
def scroll_page():
    try:
        body = driver.find_element(By.TAG_NAME, 'body')  # Grab the <body> element to send keystrokes
        body.click()  # Make sure body is active

        for _ in range(30):  # Simulate page scrolls to load more profiles
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.75)  # Small delay between scrolls for smoother loading

        # Try clicking the "Show More" button if it appears
        try:
            show_more_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, '//button[normalize-space(text())="Show more"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", show_more_button)
            time.sleep(0.5)
            show_more_button.click()
            log("🔽 Clicked 'Show More' button to load more profiles.")
            time.sleep(1)
        except:
            log("⚠️ 'Show More' button not found or not clickable.")
    except Exception as e:
        log(f"⚠️ Scroll error: {e}")

# === MAIN SCRIPT LOOP ===
try:
    time.sleep(1)  # Initial wait to let the page settle

    while True:  # Run until break condition is met
        scroll_page()  # Scroll to load more profiles
        time.sleep(0.25)  # Small pause to let elements render

        # Check if we've reached the end of available profiles
        try:
            end_message = driver.find_element(By.XPATH, '//p[contains(text(), "We have already shown you everyone.")]')
            if end_message.is_displayed():
                log("🎉 All profiles have been loaded. No more to show.")
                break  # Stop loop if end of profiles message is shown
        except:
            pass  # No end message yet — continue

        # Grab all visible profile buttons
        profile_buttons = driver.find_elements(By.CSS_SELECTOR,
            'button.outline-hidden.rounded-wds-profile-card-corner-radius')

        log(f"🔍 Found {len(profile_buttons)} profile buttons")

        new_profiles_found = 0  # Track how many new profiles were seen

        for btn in profile_buttons:
            label = btn.get_attribute("aria-label")  # This typically contains the profile name
            if not label:
                continue  # Skip if no label (not a valid profile)

            try:
                # Traverse to parent element and get location (suburb)
                parent = btn.find_element(By.XPATH, '..')
                suburb_span = parent.find_element(By.XPATH,
                    './/span[contains(@class, "text-sm") and contains(@class, "font-normal")]')
                suburb = suburb_span.text.strip()
            except Exception:
                suburb = "(suburb not found)"  # Fallback if suburb info is missing

            # Use label and suburb as a unique identifier
            profile_key = f"{label.strip().lower()} | {suburb.strip().lower()}"

            if profile_key in seen_profiles:
                continue  # Skip already seen profiles

            # Record and log new profile
            seen_profiles.add(profile_key)
            new_profiles_found += 1
            log(f"✅ New Profile: {label} 📍 {suburb}")

        if new_profiles_found == 0:
            log("🛑 No new profiles found after scrolling. Stopping script.")
            break  # If no new profiles found, exit the loop

# Handle user manually stopping the script (e.g., Ctrl+C)
except KeyboardInterrupt:
    log("\n🛑 Stopped by user manually.")
# Always clean up by closing the browser
finally:
    driver.quit()
