import os
from module.utils import log, custom_show_menu, write_txt, clean_filename
from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import re

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
    edge_options.add_argument("--mute-audio")

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
        log("INFO", "You are already logged in, skipping login process")

    log("INFO", f"Getting courses from {main_page}")

    log("INFO", f"Page title: {title}")

    sleep(2)

    driver.get(f"{main_page}pages/todos-los-cursos")

    sleep(2)

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
            driver.get(element_list[option - 1]['link'])
            course_title = element_list[option - 1]['title']
            log("INFO", f"Getting course: {course_title}")

            course_title = course_title.replace(":", " -")
            course_title = clean_filename(course_title)

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
                title_chapter = title_chapter.text.replace(":", " -")
                title_chapter = clean_filename(title_chapter)
                data_chapter = {
                    "title": title_chapter,
                    "web_element": chapter
                }

                chapter_element_list.append(data_chapter)

            for index, chapter in enumerate(chapter_element_list):
                current_path = f"{root_path}{course_title}\\{chapter['title']}"
                if not os.path.exists(current_path):
                    os.mkdir(current_path)
                    log("INFO", f"Creating directory {root_path}{course_title}")
                log("INFO", f"{index + 1} - {chapter['title']}")

                # * Get chapters from section

                chapter['web_element'].click()
                sleep(2)
                
                section_list = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ui-accordion-content-active"))
                )
                section_list_data = WebDriverWait(section_list, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "course-player__content-item"))
                )

                section_element_list = []
                for index, section in enumerate(section_list_data):
                    try:
                        chapter_section = WebDriverWait(section, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "content-item__title"))
                        )
                        chapter_section.click()
                        sleep(2)

                        chapter_section = chapter_section.text.strip().replace(":", " -").split("\n")[0]
                        chapter_section = f"{index + 1:02d} - {chapter_section}"

                        chapter_section = clean_filename(chapter_section)
                        chapter_section = chapter_section.replace("/", " -")

                        log("INFO", f"{chapter_section}")
                    except TimeoutException:
                        log("ERROR", "Element not found")
                        continue
                    try:
                        iframe = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
                        )
                        driver.switch_to.frame(iframe)
                        sleep(2)
                    except TimeoutException:
                        log("ERROR", f"No iframe found for section: {chapter_section}")
                        driver.switch_to.default_content()
                        continue

                    video_id = None
                    elementos_adicionales = driver.find_elements(By.XPATH, "//*")
                    for elemento in elementos_adicionales:
                        pattern = r'"@id":"https://fast\.wistia\.net/embed/iframe/([^"]+)"'
                        match = re.search(pattern, elemento.get_attribute('outerHTML'))
                        if match:
                            video_id = match.group(1)
                            log("INFO", f"Video ID: {video_id}")
                            break
                        else:
                            log("DEBUG", elemento.get_attribute('outerHTML'))
                    driver.switch_to.default_content()
                    if video_id is not None:
                        video_url = f"https://fast.wistia.net/embed/iframe/{video_id}"
                        log("INFO", f"Video URL: {video_url}")
                        write_txt(f"{current_path}\\{chapter_section}.txt", f"{chapter_section}\t{video_url}")
                    else:
                        log("ERROR", "Video ID not found")
                        write_txt(f"{current_path}\\{chapter_section}.txt", f"{chapter_section}\tNo disponible")
                    section_element_list.append(chapter_section)

                section_element_list = []

            close = input("[INPUT] Presione cualquier tecla para cerrar...")
            if close:
                driver.quit()
                option_continue = False
        else:
            print("[ERROR] Opción inválida")

main()