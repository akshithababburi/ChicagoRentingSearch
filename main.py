from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

CHROME_DRIVER = r"C:\Users\Akshitha\Downloads\chromedriver_win32\chromedriver.exe"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


google_form = "https://docs.google.com/forms/d/e/1FAIpQLSd7_Qmh0oqz1a-ftX9g0T1IqWxYeNEIs_qFDM-9XrOsxSandg/viewform?usp=sf_link"


ZILLOW = "https://www.zillow.com/chicago-il/rentals/?searchQueryState=%7B%22mapBounds%22%3A%7B%22north%22%3A42.05566397813515%2C%22east%22%3A-87.36801988085938%2C%22south%22%3A41.61159021630187%2C%22west%22%3A-88.09586411914063%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A17426%2C%22regionType%22%3A6%7D%5D%2C%22pagination%22%3A%7B%7D%7D"

response = requests.get(ZILLOW, headers=headers)
content = response.text

soup = BeautifulSoup(content, "html.parser")
soup.getText()

link = soup.find_all(name="a", class_="property-card-link")

address = soup.select(".StyledPropertyCardDataArea-c11n-8-85-1__sc-yipmu-0 address")
all_Add = [n.get_text().split("|")[-1] for n in address]
print(all_Add)

price = soup.find_all(name="div", class_="StyledPropertyCardDataArea-c11n-8-85-1__sc-yipmu-0")

price_list = [n.get_text().split("+")[0] for n in price if "$" in n.text]
price_list2 = [n.split("/")[0] for n in price_list]
print(price_list2)

all_links = []

for n in link:
    href = n.get("href")
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

print(all_links)

driver = webdriver.Chrome(executable_path=CHROME_DRIVER)

for n in range(len(all_links)):
    driver.get(google_form)
    time.sleep(2)
    answer1 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    answer2 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    answer3 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    answer1.send_keys(all_Add[n])
    answer2.send_keys(price_list2[n])
    answer3.send_keys(all_links[n])
    submit.click()






