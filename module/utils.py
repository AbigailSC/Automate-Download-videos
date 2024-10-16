import datetime
import os
import re

def get_datetime() -> str:
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%d-%m-%Y %H:%M")
    return formatted_date

def log(status: str, data: str):
    try:
        write_txt("LOGS.txt", f"{get_datetime()} - {status} - {data}")
    except FileNotFoundError:
        print('File not found')

def custom_show_menu(options: list[dict | str], title: str | None) -> None:
    os.system('cls')
    if title != None:
        print(f"{title}\n")
    for index in range(len(options)):
        if type(options[index]) == dict:
            print(f"{index + 1}) {options[index]["title"]}")
        else:
            print(f"{index + 1}) {options[index]}")

def write_txt(filename: str, data: str) -> None:
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(data + '\n')
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")

def clean_filename(filename: str) -> str:
    return re.sub(r'[<>:"/\\|?*¿]', '', filename)