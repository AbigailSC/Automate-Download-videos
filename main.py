import os
from module.utils import log, custom_show_menu
from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def main():
    load_dotenv()

    main_page = os.getenv("MAIN_PAGE")
    root_path = os.getenv("ROOT_PATH")

    service = Service(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")
    edge_options = webdriver.EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument("user-data-dir=C:\\Users\\Sempi\\AppData\\Local\\Microsoft\\Edge\\User Data")
    edge_options.add_argument("profile-directory=Profile 1")
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--disable-bluetooth")

    driver = webdriver.Edge(options = edge_options, service = service)

    driver.get(main_page)
    title = driver.title

    try:
        logged_in = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "header__nav-sign-in"))
        )
        if logged_in.text == "Iniciar sesión":
            element = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "header__nav-sign-in"))
            )
            element.click()
            sleep(2)
            google_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "google"))
            )
            google_button.click()
            sleep(2)
            user_account = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "VV3oRb"))
            )
            user_account.click()
    except TimeoutException:
        log("INFO", "Ya estás logueado, saltando el proceso de inicio de sesión.")

    log("INFO", f"Getting courses from {main_page}")

    log("INFO", f"Page title: {title}")

    driver.get(f"{main_page}pages/todos-los-cursos")

    sleep(5)

    courses = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "products__list-item"))
    )

    element_list = []

    for course in courses:
        title_course = course.find_element(By.TAG_NAME, "h3")
        link_course = course.find_element(By.TAG_NAME, "a")
        data_course = {
            "title": title_course.text,
            "link": link_course.get_attribute("href")
        }
        element_list.append(data_course)
    
    option_continue = True

    while option_continue:
        custom_show_menu(element_list, "[TITLE] Cursos disponibles")
        option = int(input("[INPUT] Seleccione una opción: "))

        if option > 0 and option <= len(element_list):
            driver.get(element_list[option - 1]["link"])
            course_title = element_list[option - 1]['title']
            log("INFO", f"Getting course: {course_title}")

            course_title = course_title.replace(":", " -")

            if not os.path.exists(f"{root_path}{course_title}"):
                    os.mkdir(f"{root_path}{course_title}")
                    log("INFO", f"Creating directory {root_path}{course_title}")

            resume_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Reanudar Curso"))
            )
            resume_btn.click()

            chapter_list = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "course-player__chapters-item"))
            )

            chapter_element_list = []

            for chapter in chapter_list:
                title_chapter = chapter.find_element(By.TAG_NAME, "h2")
                data_chapter = {
                    "title": title_chapter.text
                }
                chapter_element_list.append(data_chapter)

            log("INFO", "Capítulos disponibles")
            for index, chapter in enumerate(chapter_element_list):
                log("INFO", f"{index + 1}. {chapter['title']}")
            option_continue = False
        else:
            print("[ERROR] Opción inválida")

main()