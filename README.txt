# 🕵️‍♂️ Skout Profile Scraper (Selenium)

This script uses **Selenium WebDriver** to automate the process of loading and extracting visible profile information from the [Skout](https://www.skout.com/) website. It scrolls the page, clicks "Show More" buttons, and logs new profiles to a file.

> ⚠️ This tool is intended for **educational and personal automation** use only. Please comply with Skout's [Terms of Service](https://www.skout.com/terms.html) before using this script.

---

## 📋 Features

- Automatically scrolls the page to load more profiles
- Detects when all profiles have been displayed
- Logs new, unseen profile names and locations to `profiles1.txt`
- Uses existing Chrome user data to maintain login sessions

---

## 🔧 Prerequisites

Before running the script, you’ll need to install the following:

### 1. Python 3.7 or newer  
You can download Python from: https://www.python.org/downloads/

### 2. Required Python Packages  
Install dependencies using pip:

```bash
pip install selenium python-dotenv
```

### 3. Chrome Browser  
Download Chrome (if not already installed):  
https://www.google.com/chrome/

### 4. ChromeDriver  
Make sure the ChromeDriver version matches your installed Chrome version.  
Download it here: https://chromedriver.chromium.org/downloads

Unzip it and place it somewhere on your local drive. Keep track of the full path to `chromedriver.exe`.

---

## ⚙️ Environment Setup

Create a `.env` file in the project directory to store your local paths:

```env
CHROME_DRIVER_PATH=C:\Path\To\chromedriver.exe
CHROME_BINARY_PATH=C:\Path\To\chrome.exe
USER_DATA_DIR=C:\Path\To\Chrome\User\Data
```

**Important Notes:**
- The paths **must not** be quoted or prefixed with `r""` in the `.env` file.
- `USER_DATA_DIR` should point to a Chrome profile directory that has previously logged in to Skout.

> You can find your Chrome user data by navigating to `chrome://version/` in Chrome and checking the "Profile Path".

---

## 🚀 Running the Script

Once everything is set up, run the script from your terminal or command prompt:

```bash
python SKOUT.py
```

The script will:
- Open Chrome with your profile
- Navigate to Skout
- Attempt login (if not already logged in)
- Scroll and extract profiles
- Write new entries to `profiles1.txt`

---

## 📁 Output

All discovered profiles will be logged to `profiles1.txt` in the following format:

```
✅ New Profile: JaneDoe 📍 Sydney
```

---

## 🔒 Security Note

To keep your environment variables secure:
- **Do not** upload `.env` files to GitHub
- Add this to your `.gitignore`:

```gitignore
.env
profiles1.txt
```

---

## 🧠 Troubleshooting

- **Driver not found?** Make sure the `CHROME_DRIVER_PATH` is correct and points to the actual `.exe`.
- **Blank Chrome opens?** Double-check your `CHROME_BINARY_PATH` and `USER_DATA_DIR` paths.
- **Stuck on login?** Make sure you're already logged in via the Chrome profile you selected.

---

## ✅ License

MIT License – Feel free to use and adapt, but respect Skout's platform terms.
