from main_data import get_main_data
from additional_data import get_additional_data

def main():
    while True:
        task = int(input("Select an action (1/2):\n"
                "\t1 - get basic information about the model\n"
                "\t2 - get additional information about the model\n"
                "\t3 - exit\n"))

        if task == 1:
            url = input("Enter link: ")
            spreadsheet_id = input("Enter spreadsheet id: ")
            get_main_data(url, spreadsheet_id)
        elif task == 2:
            spreadsheet_id = input("Enter spreadsheet id: ")
            get_additional_data(spreadsheet_id)
        else:
            break

if __name__ == '__main__':
    main()