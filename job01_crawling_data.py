from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')

driver = webdriver.Chrome(options = options)
url = 'https://kiss.kstudy.com/search/sch-result.asp'
driver.get(url)
time.sleep(10)
# check_2022 = '//*[@id="mCSB_2_container"]/div[1]/label/input'
# driver.find_element('xpath', check_2022).click()
# # time.sleep(2)
# check_2021 = '//*[@id="mCSB_2_container"]/div[2]/label/input'
# driver.find_element('xpath', check_2021).click()
# time.sleep(2)
check_2020 = '//*[@id="mCSB_2_container"]/div[3]/label/input'
driver.find_element('xpath', check_2020).click()
time.sleep(2)
check_kci = '//*[@id="mCSB_3_container"]/div[2]/label/input'
driver.find_element('xpath', check_kci).click()
time.sleep(2)
btn_search = '//*[@id="btnGroupBy2"]'
driver.find_element('xpath', btn_search).click()
time.sleep(2)


# 1~10
abstracts = []
titles = []
list_address = []
for page in range (1, 11):
    page_xpath = '//*[@id="right"]/div[2]/a[{}]'.format(page)
    driver.find_element('xpath', page_xpath).click()
    time.sleep(2)
    for count in range (1, 29, 3): # 29
        try:
            title_xpath = '//*[@id="form_main"]/table/tbody/tr[{}]/td[2]/div/div[1]/h5/a'.format(count)
            title = driver.find_element('xpath', title_xpath).text
            titles.append(title)

            driver.find_element('xpath', title_xpath).send_keys(Keys.ENTER)
            time.sleep(5)
            driver.switch_to.window(driver.window_handles[-1])

            key_word_xpath = '//*[@id="contents"]/div/div[1]/div[1]/section[3]/div'
            key_word = driver.find_element('xpath', key_word_xpath).text

            abstract_xpath = '//*[@id="contents"]/div/div[1]/div[1]/section[4]/div[1]'
            abstract = driver.find_element('xpath', abstract_xpath).text

            address = driver.current_url
            list_address.append(address)
            print(address)

            review = key_word + ' ' + abstract
            abstracts.append(review)
            print(1, page)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(2)


        except:
            print('error', page, (count//3)+1)




    print(abstracts)
    print(titles)
    print(list_address)
    df = pd.DataFrame({'titles': titles, 'abstracts': abstracts})
    if page % 5 == 0:
        df.to_csv('./crawling_data/reviews_2020_1_{}page.csv'.format(page), index=False)

next_xpath = '//*[@id="right"]/div[2]/a[11]'
driver.find_element('xpath', next_xpath).click()
time.sleep(2)

# 11 ~ 100
for i in range (2, 11):
    abstracts = []
    titles = []
    list_address = []
    for page in range(3, 13):
        page_xpath = '//*[@id="right"]/div[2]/a[{}]'.format(page)
        driver.find_element('xpath', page_xpath).click()
        time.sleep(2)
        for count in range(1, 29, 3):
            try:
                title_xpath = '//*[@id="form_main"]/table/tbody/tr[{}]/td[2]/div/div[1]/h5/a'.format(count)
                title = driver.find_element('xpath', title_xpath).text
                titles.append(title)

                driver.find_element('xpath', title_xpath).send_keys(Keys.ENTER)
                time.sleep(5)
                driver.switch_to.window(driver.window_handles[-1])

                key_word_xpath = '//*[@id="contents"]/div/div[1]/div[1]/section[3]/div'
                key_word = driver.find_element('xpath', key_word_xpath).text

                abstract_xpath = '//*[@id="contents"]/div/div[1]/div[1]/section[4]/div[1]'
                abstract = driver.find_element('xpath', abstract_xpath).text

                address = driver.current_url
                list_address.append(address)

                review = key_word + ' ' + abstract
                abstracts.append(review)
                print(i, page)

                driver.switch_to.window(driver.window_handles[-1])
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)

            except:
                print('error', page, (count // 3) + 1)



        print(abstracts)
        print(titles)
        df = pd.DataFrame({'titles': titles, 'abstracts': abstracts})
        if (page-2) % 5 == 0:
            df.to_csv('./crawling_data/reviews_2020_{}_{}page.csv'.format(i, page-2), index=False)
        if (page-2) == 10 :
            next_xpath = '//*[@id="right"]/div[2]/a[13]'
            driver.find_element('xpath', next_xpath).click()
            time.sleep(2)








    # except NoSuchElementException as e:
    #     print('None', (title//3)+1)
    #     driver.switch_to.window(driver.window_handles[-1])
    #     driver.close()
    #     driver.switch_to.window(driver.window_handles[0])
    #     time.sleep(2)
    #     chrome_return_tap






# check_2022 = '//*[@id="mCSB_2_container"]/div[1]/label/span[1]'
# driver.find_element('xpath', check_2022).click
# time.sleep(0.2)
# check_2021 = '//*[@id="mCSB_2_container"]/div[2]/label/span[1]'
# driver.find_element('xpath', check_2021).click
# time.sleep(0.2)
# check_2020 = '//*[@id="mCSB_2_container"]/div[3]/label/span[1]'
# driver.find_element('xpath', check_2020).click
# time.sleep(0.2)
# check_kci = '//*[@id="mCSB_3_container"]/div[2]/label/span[1]'
# driver.find_element('xpath', check_kci).click
# time.sleep(0.2)
# btn_search = '//*[@id="btnGroupBy2"]'
# driver.find_element('xpath', btn_search).click
# time.sleep(1)


# //*[@id="contents"]/div/div[1]/div[1]/section[4]/div[2]/pre
# options = webdriver.ChromeOptions()
# options.add_argument('lang=ko_KR')
#
# driver = webdriver.Chrome(options = options)
#
# for page in range(1,32):
#     url = ''.format(your_year, page)
#     titles = []
#     reviews = []
#     try:
#         for title_num in range(1 ,21):
#             driver.get(url)
#             time.sleep(0.5)
#             movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(title_num)
#             title = driver.find_element('xpath', movie_title_xpath).text
#             driver.find_element('xpath', movie_title_xpath).click()
#             time.sleep(0.1)
#             try:
#                 driver.find_element('xpath', review_button_xpath).click()
#                 time.sleep(0.1)
#                 review_num = driver.find_element('xpath', review_num_path).text
#                 review_num = review_num.replace(',', '')
#                 review_range = (int(review_num) - 1)// 10 + 1
#                 if review_range > 3:
#                     review_range = 3
#
#                 for review_page_num in range (1, review_range + 1):
#                     review_page_button_xpath = '// *[ @ id = "pagerTagAnchor{}"]'.format(review_page_num)
#                     driver.find_element('xpath', review_page_button_xpath).click()
#                     time.sleep(0.1)
#
#                     for review_title_num in range(1,11):
#                             review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a'.format(review_title_num)
#                             driver.find_element('xpath', review_title_xpath).click()
#                             time.sleep(0.1)
#                             try:
#                                 review = driver.find_element('xpath', review_xpath).text
#                                 titles.append(title)
#                                 reviews.append(review)
#                                 print(title)
#                                 print(review)
#                                 driver.back()
#                             except:
#                                 print('review',page, title_num, review_title_num)
#                                 driver.back()
#             except:
#                 print('review button', page, title_num)
#
#
#         df = pd.DataFrame({'titles':titles, 'reviews':reviews})
#         df.to_csv('./crawling_data/reviews_{}_{}page.csv'.format(your_year, page), index=False)
#
#     except:
#         print('error', page, title_num)
#
#
#