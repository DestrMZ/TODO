import os
import bot_commands as commands
from telebot import types

bot = commands.bot


COMMAND_MAP = {
    'new_item': commands.add_item,
    'all': commands.show_all_items,
    'delete': commands.delete_item,
    'refresh': commands.refresh_tasks,
}


NP_COMMAND = ('all', 'refresh')

INFO = '''

/start - идентификация пользователя
/new_item <название задачи> - добавить новую задачу
/all - посмотреть весь список задач
/delete <номер задачи> - удалить задачу
/refresh - изменить номер списка задач на номера от 1 по порядку
/info - информация о боте
'''

welcome_info = '''
Я ваш персональныый менеджер задач, вы можете добавить, удалить или обновить Ваш список дел!
'''

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, f'Добро пожаловать, {message.from_user.first_name}.')
    bot.send_message(user_id, welcome_info)
    bot.send_message(user_id, INFO)
    task_dir = f'TODO/{user_id}'
    if not os.path.exists(f'TODO/{user_id}'):
        # отсылаем информацию пользователю о боте, если то ещё не был идентифицирован
        bot.send_message(user_id, INFO)
        os.makedirs(f'TODO/{user_id}', exist_ok=True)
        with open (os.path.join(task_dir, 'tasks.csv'), 'w', newline='') as tasks_file:
            # add title
            commands.csv.writer(tasks_file).writerow(('id', 'description'))

    
@bot.message_handler(commands=['info'])
def info_handler(message):
    bot.send_message(message.from_user.id, INFO)


@bot.message_handler(commands=COMMAND_MAP.keys()) # type: ignore
def commands_handler(message):
    user_id = message.from_user.id
    if os.path.exists(f'TODO/{user_id}'):
        params = message.text.split(' ', 1)
        command_name = params.pop(0)[1:]
        if command_name in NP_COMMAND:
            COMMAND_MAP[command_name](user_id)
        else:
            try:
                COMMAND_MAP[command_name](user_id, *params)
            except TypeError:
                bot.send_message(user_id, 'Команда была использована неправильно. Воспользуйтесь командой /info')
    else:
        bot.send_message(user_id, 'Пользователь не инициализирован! /start')


bot.polling()