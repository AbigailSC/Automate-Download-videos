import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from module.utils import log
from time import sleep

load_dotenv()

main_page = os.getenv("MAIN_PAGE")
navigator = os.getenv("NAVIGATOR")

service = Service(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")
edge_options = webdriver.EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument("user-data-dir=C:\\Users\\Sempi\\AppData\\Local\\Microsoft\\Edge\\User Data")
edge_options.add_argument("profile-directory=Profile 1")
edge_options.add_argument("--start-maximized")

driver = webdriver.Edge(options = edge_options, service = service)

driver.get('https://cursos.devtalles.com/pages/todos-los-cursos')

title = driver.title

log("INFO", f"Getting courses from {main_page}")
log("INFO", f"Page title: {title}")

element_list = []

courses = driver.find_elements(By.CLASS_NAME, "products__list-item")

for course in courses:
    element_list.append(course.text)
    title_course = course.find_element(By.TAG_NAME, "h3")
    log("INFO", f"Course: {title_course.text}")

driver.close()