# Telegram cocktail bot  
<img width="295" alt="image" src="https://user-images.githubusercontent.com/60853743/167307541-c4d21f5b-4582-4a93-8f89-898c1faf2b03.png">

Библиотека: pyTelegramBotAPI
____________________________

## Описание бота
Этот бот хранит в себе меню коктейлей и по команде может выдать нужный рецепт.
Также есть возможность выбора случайного коктейля из имеющихся.

## Разбор интерфейса и технических решений

### 1. Обработчик команды **/start**
Обработчик срабатывает, когда пользователь начинает взаимодействие с ботом. 

```py
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, menu_messages.start_menu,
                                      parse_mode='html')
    start_keyboard = types.InlineKeyboardMarkup()
    show_commands = types.InlineKeyboardButton(text='Команды' + '\U0001F4CB	', callback_data='ShowCommands')
    start_keyboard.add(show_commands)
    bot.send_message(message.chat.id, menu_messages.start_button, reply_markup=start_keyboard)
```
На экран выводятся приветствие и кнопка с приглашением ознакомиться с существующими командами.

<img width="423" alt="image" src="https://user-images.githubusercontent.com/60853743/167307085-4fad61f3-0f19-4367-8e82-c774c2d8c343.png">

К кнопке привязан callback-обработчик, выдающий пользователю сообщение со списком доступных команд.

```py
@bot.callback_query_handler(func=lambda c: c.data)
def answer_callback(callback):
    if callback.data == 'ShowCommands':
        bot.send_message(callback.message.chat.id, menu_messages.calback_button,
                                                   parse_mode='html')
```

Результат срабатывания обработчика

![image](https://user-images.githubusercontent.com/60853743/167307386-d017b6d0-631c-416d-a071-ab2bcfb1dcd1.png)

## 2. Словари с данными о коктейлях
В модели всего 3 словаря с одинаковыми ключами. Они хранят в себе название, рецепт и ссылку на коктейль.

```py
cocktail_name = {'/pinacolada':  '«Пина Колада»',
                 '/mojito':      '«Мохито»',
                 ...
                 
                 ...
                 }


cocktail_link = {'/pinacolada':  'https://ru.wikipedia.org/wiki/%D0%9F%D0%B8%D0%BD%D0%B0_%D0%BA%D0%BE%D0%BB%D0%B0%D0%B4%D0%B0',
                 '/mojito':      'https://ru.wikipedia.org/wiki/%D0%9C%D0%BE%D1%85%D0%B8%D1%82%D0%BE',
                 ...
                 
                 ...
                 }


cocktail_recipe = {'/pinacolada':  f'<b>Рецепт {cocktail_name["/pinacolada"]}:</b>\n'
                                   '<b>1. </b>Ром - 70мл\n'
                                   '<b>2. </b>Ананасовый сок - 100мл\n'
                                   '<b>3. </b>Кокосовое молоко - 35мл\n'
                                   '<b>4. </b>Кокосовый сироп - 1ст.л\n'
                                   ...
                                   
                                   ...
                   }
```

## 3. Основная функция, выводящая всю информацию о коктейле
Обработчик срабатывает если текст сообщения соответствует команде **/random** или под указанным ключём есть запись в словаре.
В зависимости от входного условия функция выводит в ответном сообщении случайный либо указанный коктейль. А также фото к нему
и ссылку, пройдя по которой можно узнать больше информации о напитке и способе его приготовления.

```py
@bot.message_handler(content_types=['text'],
func = lambda message: message.text == '/random' or message.text in cocktail_dict.cocktail_name)
def random_cock(message, my_key=get_random_key()):
    if message.text == '/random':
        my_key = get_random_key()
    elif message.text in cocktail_dict.cocktail_name:
        my_key = message.text

    photo = open('photos' + my_key + '.png', 'rb')
    bot.send_photo(message.chat.id, photo, 'Коктейль ' + cocktail_dict.cocktail_name[my_key])
    bot.send_message(message.chat.id, cocktail_dict.cocktail_recipe[my_key], parse_mode='html')
    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text=cocktail_dict.cocktail_name[my_key],
                                             url=cocktail_dict.cocktail_link[my_key])
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, menu_messages.pre_link_button, reply_markup=markup)
```

Результаты срабатывания

![image](https://user-images.githubusercontent.com/60853743/167308075-9ed4ebf4-6e2d-49d8-94dd-59b147a0201b.png)
![image](https://user-images.githubusercontent.com/60853743/167308117-58d479d7-3dbf-4b47-9bfb-1f0a1afff19c.png)

## 4. Переход по ссылке
Ссылка, указанная после рецепта ведёт на сайт wikipedia.org

<img width="228" alt="image" src="https://user-images.githubusercontent.com/60853743/167308194-d0e57960-9860-4e5b-8ea5-457b5e90457e.png">
<img width="241" alt="image" src="https://user-images.githubusercontent.com/60853743/167308216-de4a4dc8-f9e4-441c-9b46-e879db8c867c.png">

