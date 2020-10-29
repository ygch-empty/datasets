# -*- coding: utf-8 -*-
"""
Created on Tue May 19 09:35:24 2020

@author: songxy
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from lxml import etree
import time
import re
from ways import get_data
import random

def pasre_page(driver):
    html = etree.HTML(driver.page_source)
    trs = html.xpath('//tr[@bgcolor]')
    for tr in trs:
        title = tr.xpath('./td//a[@class="fz14"]/text()')[0]
        authors = tr.xpath('./td[@class="author_flag"]/a[@class="KnowledgeNetLink"]//text()')
        authors = "|".join(authors)
        source = tr.xpath('./td//a[@target="_blank"]/text()')[1]
        times = tr.xpath('./td[@align="center"]/text()')[0].strip()
        database = tr.xpath('./td[@align="center"]/text()')[1].strip()
        counted = tr.xpath('./td//span[@class="KnowledgeNetcont"]/a/text()')
        if len(counted) == 0:
            counted = 0
        else:
            counted = counted[0]
        downloadCount = tr.xpath('./td//span[@class="downloadCount"]/a/text()')
        if len(downloadCount) == 0:
            downloadCount = 0
        else:
            downloadCount = downloadCount[0]
        data = {
                "title":title,
                "authors":authors,
                "source":source,
                "times":times,
                "database":database,
                "counted":counted,
                "downloadCount":downloadCount,
                }
        datas.append(data)
        print(title)
    time.sleep(random.uniform(2,4))
    driver.switch_to.parent_frame()
    search_win = driver.find_element_by_id('expertvalue')
    search_win.clear()
    time.sleep(random.uniform(2,4))
    
if __name__ == '__main__':

    datas = [u"温度", u"压力", u"湿度"]
    driver_path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    url = "https://www.cnki.net/"
    driver.get(url)

    home_page = driver.find_element_by_id('highSearch')
    home_page.click()
    driver.switch_to.window(driver.window_handles[1])
    # 查找左边文献分类目录，并清除所选中的学科
    driver.find_element_by_xpath("//div[@id='XuekeNavi_Div']/div[1]/input[1]").click()
    # 查找基础学科并展开，然后选择海洋学学科
    driver.find_element_by_id("Afirst").click()
    html = WebDriverWait(driver, 30).until(expected_conditions.presence_of_all_elements_located((By.ID, 'A010second')))
    html[0].find_element_by_xpath("following-sibling::input[1]").click()

    for data in datas:
        # 查找查询主题文本框，并设置值，汉字必须为Unicode编码格式
        theme = driver.find_element_by_id("txt_1_value1")
        theme.clear()
        theme.send_keys(data)
        driver.find_element_by_id("txt_1_value2").click()
        driver.execute_script("document.getElementById('__droplist').style.display = 'none';")
        # 获取查询按钮，并点击查询
        search_btn = driver.find_element_by_id("btnSearch")
        search_btn.click()
        # 切换到查询结果的iframe
        resultDriver = driver.find_element_by_id('iframeResult')
        driver.switch_to.frame(resultDriver)
        # 等待数据检索结果，如果100s之内不返回，则自动放弃
        time.sleep(50)
        # WebDriverWait(driver, 100).until(expected_conditions.presence_of_all_elements_located((By.ID, 'J_ORDER')))
        records = driver.find_element_by_xpath("//div[@class='pageBar_min']/div[@class='pagerTitleCell']").text
        # 去掉查找结果内容的汉字
        records = records.encode("utf8").strip().replace("找到 ", "").replace(" 条结果", "")
        # 去掉数字中间的逗号分隔符
        record = records.replace(",", "")
        print(int(record))
        driver.switch_to.default_content()

# results = get_data()
# for result in results:
#     search_win = driver.find_element_by_id('expertvalue')
#     search_win.send_keys(result)
#     search_btn = driver.find_element_by_id('btnSearch')
#     search_btn.click()
#     iframe = driver.find_element_by_id('iframeResult')
#     driver.switch_to.frame(iframe)
#     time.sleep(random.uniform(2,4))
#     pasre_page(driver)
