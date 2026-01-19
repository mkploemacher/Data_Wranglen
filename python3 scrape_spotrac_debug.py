import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_spotrac_cash_total(
    year: int = 2020,
    chromedriver_path: str = "/opt/homebrew/bin/chromedriver",
    headless: bool = False,
    timeout: int = 15
) -> pd.DataFrame:
    """
    Scrape NBA cash‐total rankings from Spotrac.
    Returns a DataFrame with ['Rank','Player','CashTotal'].
    """
    print("Working directory:", os.getcwd())

    # 1) Start Chrome
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=opts)

    try:
        # 2) Go to the page
        url = f"https://www.spotrac.com/nba/rankings/player/_/year/{year}/sort/cash_total"
        print("Navigating to", url)
        driver.get(url)

        wait = WebDriverWait(driver, timeout)

        # 3) Dismiss cookie banner if present
        try:
            btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#ez-accept-all")))
            btn.click()
            print("✔️ Accepted cookies")
        except TimeoutException:
            # no banner showed up within a few seconds
            pass

        # 4) Wait for the table wrapper to appear
        try:
            table = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.datatable"))
            )
        except TimeoutException:
            print("❌ Could not find the datatable!")
            print("--- HTML Snippet ---")
            print(driver.page_source[:2000])
            raise

        # 5) Grab all the rows
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        print(f"✅ Found {len(rows)} rows")

        # 6) Parse rank, name, cash into a list
        records = []
        for row in rows:
            rank    = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
            name    = row.find_element(By.CSS_SELECTOR, "td:nth-child(2) a").text.strip()
            cash    = row.find_elements(By.TAG_NAME, "td")[-1].text.strip()
            records.append({"Rank": rank, "Player": name, "CashTotal": cash})

        # 7) Build a DataFrame
        df = pd.DataFrame(records, columns=["Rank","Player","CashTotal"])
        print(df.head(10))
        return df

    finally:
        driver.quit()


if __name__ == "__main__":
    # set headless=True if you don't want to watch the browser pop up
    df = scrape_spotrac_cash_total(year=2020, headless=False)
    df.to_csv("nba_cash_totals_2020.csv", index=False)
