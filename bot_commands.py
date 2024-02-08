import telebot
import csv
import os

# with open('token.txt', 'r') as token_file:
#     TOKEN = token_file.read()

TOKEN = '6302412593:AAEgDhdSw1_GJCFRhCFcofdyFh1-cpkJxNQ'
bot = telebot.TeleBot(TOKEN)


def add_item(user_id, item):
    user_directory = f'TODO/{user_id}'
    os.makedirs(user_directory, exist_ok=True)
    print(user_directory)


    # with open(f'{user_directory}/tasks.csv', 'a+', newline='', encoding='utf-8') as tasks_file:
    with open('tasks.csv', 'a+', newline='', encoding='utf-8') as tasks_file:
        tasks_file.seek(0)
        data = list(csv.DictReader(tasks_file))

        new_id = 1 if not data else int(data[-1]['id']) + 1
        writer = csv.DictWriter(tasks_file, fieldnames=('id', 'discription'))
        if not data:
            writer.writeheader()
        tasks_file.seek(0, 2)
        writer.writerow({'id': new_id, 'discription': item})   
    
    bot.send_message(user_id, f'Задача {item}, была успешно создана! Под номером {new_id}')


# def add_item(user_id, task_description):
    # Путь к директории и файлу, куда записываются задачи
    # tasks_path = 'tasks.csv'
    
    # # Создание директории и файла, если они еще не существуют
    # os.makedirs(os.path.dirname(tasks_path), exist_ok=True)
    
    # # Открытие файла для записи новой задачи
    # with open(tasks_path, 'a', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow([task_description])  # Запись описания задачи


    # with open(f'TODO/{user_id}/tasks.csv', 'r+', newline='') as tasks_file:
    #     # для номера новой задачи выбираем номер последней задачи +1
    #     data = list(csv.DictReader(tasks_file))
    #     if data:
    #         new_id = int(data[-1]['id']) + 1
    #     else:
    #         new_id = 1
    #     csv.DictReader(tasks_file, fieldnames=('id', 'description')).writerow({'id': new_id, 'description': item})
    # bot.send_message(user_id, f'Задача {item} была успешно добавлены в ваш список под номеремо {new_id}')


def show_all_items(user_id):
    task_list = ''
    with open('tasks.csv', 'r', newline='') as tasks_file:
        reader = csv.DictReader(tasks_file)
        for row in reader:
            task_list += f"{row['id']}, {row['discription']}\n"
    if task_list:
        bot.send_message(user_id, task_list)
    else:
        bot.send_message(user_id, 'У вас ещё нет задач!')


def delete_item(user_id, item_id):
    new_data = []
    found = False

    with open('tasks.csv', 'r', newline='') as inp:
        for row in csv.DictReader(inp):
            if row['id'] == item_id:
                found = True
                print('Yes inp')
            else:
                print(new_data)
                new_data.append(row)
                print(new_data)


    if found:
        with open('tasks.csv', 'w', newline='') as out:
            writer = csv.DictWriter(out, fieldnames=('id', 'discription'))
            writer.writeheader()
            writer.writerows(new_data)
        bot.send_message(user_id, f'Задача по номером {item_id} была успешно удалена!')
    else:
        bot.send_message(user_id, f'Задачи под номером {item_id} нет в вашем списке!')


def refresh_tasks(user_id): # update number ls
    new_data = []

    with open('tasks.csv', 'r', newline='') as inp:
        for i, row, in enumerate(csv.DictReader(inp)):
            row['id'] = i
            new_data.append(row)
            print('This is 101 ROW - ', row, new_data)
    
    with open('tasks.csv', 'w', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=('id', 'discription'))
        writer.writeheader()
        writer.writerows(new_data)
    bot.send_message(user_id, f'Номера ваших задач обновлены!')
