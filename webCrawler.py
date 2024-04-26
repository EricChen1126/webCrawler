from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, json

url = 'https://rent.591.com.tw/?region=3&section=34&searchtype=1&multiPrice=20000_30000'
driver = webdriver.Chrome('./chromedriver.exe')
driver.implicitly_wait(10)
driver.get(url)

folder = []
count = 0
page = 1

while True:
    print("正在抓: " + str(page) + "頁 的網路資料 ~ ~")
    page += 1
    soup = BeautifulSoup(driver.page_source, 'lxml')
    tag_sec = soup.select_one("section.vue-list-rent-content > div")
    tag_list = tag_sec.find_all("section")
    for tag_li in tag_list:
        title = tag_li.find("div", class_="item-title")
        price = tag_li.find("div", class_="item-price-text").find("span")
        folder.append({"id": count,
            "title": title.text,
            "price": str(price),})
        count += 1
        print("已取得:", count, "筆資料!")

    button_css = "section.vue-public-list-page > div > a.pageNext"
    button = driver.find_elements(By.CSS_SELECTOR, button_css)

    # 尋找 "下一頁" 的按鈕
    if button[len(button) -1].text == "下一頁":
        if (count-1) % 30 == 0:
            button[len(button) -1].click()
        else:
            break
    else:
        break
    time.sleep(10)

driver.quit()

# 存檔成Json檔
with open("591House.json", "w", encoding="utf-8") as fp:
    json.dump(folder, fp, indent=2, sort_keys=True, ensure_ascii=False)
