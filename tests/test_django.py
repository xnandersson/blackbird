from selenium import webdriver
browser = webdriver.Firefox()
browser.get('htt.//localhost:8000')
assert 'Django' in browser.title 
