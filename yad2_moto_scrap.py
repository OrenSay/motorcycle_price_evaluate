# -*- coding: utf-8 -*-
"""

@author: orens
"""
# %%
from selenium import webdriver

path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)

driver.get('https://www.yad2.co.il/vehicles/motorcycles')

# %%
import pandas as pd
import time

columns = ['maker', 'model', 'category', 'year', 'hand', 'size', 'price', 'location', 'km', 'lising', 'test', 'licence',
           'dealer', 'origin', 'color']
df = pd.DataFrame()
table = driver.find_element_by_class_name('feed_list')

# %%
for j in range(25):
    for i in range(0, 17):
        try:
            title = driver.find_element_by_xpath('//*[@id="feed_item_%s_title"]/span' % i)
            maker = title.text.split(' ')[0]
            model = title.text.split(' ', 1)[1]
            sub = driver.find_element_by_xpath('//*[@id="feed_item_%s"]/div[1]/div[1]/div[2]/span[2]' % i)
            cat = sub.text
            price = driver.find_element_by_xpath('//*[@id="feed_item_%s_price"]' % i).text
            year = driver.find_element_by_xpath(' //*[@id="data_year_%s"]' % i).text
            hand = driver.find_element_by_xpath('//*[@id="data_hand_%s"]' % i).text
            cc = driver.find_element_by_xpath('//*[@id="data_engine_size_%s"]' % i).text
            dealer = driver.find_element_by_xpath('//*[@id="feed_item_%s_date"]' % i).text
            detail = driver.find_element_by_xpath('//*[@id="feed_item_%s"]' % i)
            detail.click()
            time.sleep(1)
            location = driver.find_element_by_xpath(
                '//*[@id="accordion_wide_%s"]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/div/span[2]' % i).text
            km = driver.find_element_by_xpath(
                '//*[@id="accordion_wide_%s"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/dl[1]' % i).text
            licence = driver.find_element_by_xpath(
                '//*[@id="accordion_wide_%s"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/dl[2]' % i).text
            color = driver.find_element_by_xpath(
                '//*[@id="accordion_wide_%s"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/dl[3]' % i).text
            test = driver.find_element_by_xpath(
                '//*[@id="accordion_wide_%s"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/dl[4]' % i).text
            lising = driver.find_element_by_xpath(
                '//*[@id="accordion_wide_%s"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/dl[5]' % i).text
        except Exception:
            continue
        s = {'maker': maker, 'model': model, 'categorty': cat, 'year': year, 'hand': hand, 'size': cc, 'price': price
            , 'location': location, 'km': km, 'lising': lising, 'test': test, 'licence': licence, 'dealer': dealer,
             'color': color}
        df = df.append(s, ignore_index=True)
    try:
        link = driver.find_element_by_link_text('הבא')
        link.click()
        time.sleep(10)
    except Exception:
        time.sleep(10)
        link = driver.find_element_by_link_text('הבא')
        link.click()
        time.sleep(10)

# %%
df.to_csv('yad2_moto.csv', index=False)
# %%
driver.quit()