from selenium import webdriver
import sys
driver = webdriver.Chrome(
    'C:/Users/user/Documents/wetube/src/chromedriver.exe')

url = sys.argv[1]
driver.get(url)
