from datetime import datetime


def print_log(text):
    date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("> {0} => {1}".format(date_now, text))