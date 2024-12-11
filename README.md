# pars_torgigovru

### Установить зависимости: 

pip install -r requirements.txt

### создать файл .env, в нем прописать переменную BOT_API=""

### В файле `admin.py` прописать id админа (id в телеграмме) в строке `router.message.filter(ChatFilter([<id>]))` 

### Запустить `main.py`

### Логика:
При каждом запуске необходимо отправлять команду `start`, чтобы установить начальные параметры.

#### Кнопка `Лоты` выводит список лотов из бд.
- Кнопка `Анализ` сравнивает цену из лота с ценой похожих объявлений на соответствующей площадке (для авто - auto.ru, для недвижимости - cian.ru)
- Кнопка `Добавить в избранное` добавляет лот в "избранное"
#### Кнопка `Обновить все лоты` загружает все новые лоты. Так как все лоты упорядочены, при попытке добавить существующий лот, добавление прекращается.
#### Кнопка `Избранное` выводит избранные лоты
- Кнопка `Удалить из избранного` удаляет лот из избранного
#### Кнопка `Фильтр` выводит фильтры.
- Кнопка `Регион` позволяет выбрать регион местонахождения лота
- Кнопка `Категория` позволяет выбрать категорию (автомобили или недвижимость)

#### Кнопки `>>` `<<` показывают следующую "страницу"/лот
#### Кнопка 'Назад' возвращает на меню выше


