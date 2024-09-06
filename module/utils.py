import datetime

def get_datetime() -> str:
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%d-%m-%Y %H:%M")
    return formatted_date

def log(status: str, data: str):
    try:
        with open("LOGS.txt", "a") as file:
            line = f"{get_datetime()} [{status}] - {data}"
            file.write(line + '\n')
    except FileNotFoundError:
        print('File not found')