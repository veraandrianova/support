Клонирование проекта
git clone git@github.com:veraandrianova/support.git

Установка зависимостей
pip install -r requirements.txt


Настройка отправки сообщений в телеграмм канал
1. Сделайте канал публичным, установите для него username.
2. Добавьте в канал любого бота.
3. Перейдите по ссылке https://api.telegram.org/bot[ТОКЕН_БОТА]/sendMessage?chat_id=@[USERNAME_КАНАЛА]&text=тест
После перехода по ссылке будет выведен id канала, сохраните его.
пример:
   {"ok":true,"result":{"message_id":57,"sender_chat":{"id":-1001658312828,"title":"Test_2","username":"testtestchannels","type":"channel"},"chat":{"id":-1001658312828,"title":"Test_2","username":"testtestchannels","type":"channel"},"date":1662541079,"text":"\u0442\u0435\u0441\u0442"}}
id: -1001658312828   
4. Сделайте канал приватным.

ДО ЗАПУСКА ПРОЕКТА ЗАПОЛНИТЬ ФАЙЛ token.py тремя переменными api_token, channel_id, host

1. Отправка сообщения осуществляется в services.py
- изменить api_token на токен бота и channel_id на id из настройки отправки сообщений в телеграмм канал пускт 3

2. Добавить db вместо sqlite в настройках

3. Создать суперпользователя для назначения is_staff и просмотра рейтинга

4. Отсутвует автозакрытие чата

5. Отсутвует логика примема изображения

6. Есть поле star_3 модели Rating для расширения возможности оценки

7. Подключить статику на сервере.

8. Чтобы работали сокеты, используется брокер redis, его host в settings.py CHANNEL_LAYERS

9. Если бы данное приложение разворачивалось в docker, то есть docker-compose.yaml и dockerfile, если нет,
то нужно настроить host брокера

10. redis! если он уже запущен на сервере, его же нужно и подлючить!

11. Зайти в контейнер и создать суперпользователя docker-compose run webapp python manage.py createsuperuser

12. Заходим по суперпользователю в admin панель, модель RatingStar. Создать пять обьектов(1 звезда, 2 звезды и т.д.)
и сохранить их.


