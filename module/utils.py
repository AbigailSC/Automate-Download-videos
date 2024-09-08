import datetime
import os

def get_datetime() -> str:
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%d-%m-%Y %H:%M")
    return formatted_date

def log(status: str, data: str):
    try:
        with open("LOGS.txt", "a", encoding="utf-8") as file:
            line = f"{get_datetime()} [{status}] - {data}"
            file.write(line + '\n')
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