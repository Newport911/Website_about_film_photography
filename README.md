# Новостной сайт о пленочной фотографиию

### Обзор
Проект Film — это веб-приложение на базе Django, предназначенное для управления и отображения новостных статей о пленочной
фотографии. Включает в себя такие функции, как поиск, списки статей по тэгу, редактор статей с отложенной публикацией страницы 
с детальным описанием.

### Особенности  
- Поиск 
- Тэги для статей
- Список статей по тэгу
- Редактор с отложенной публикацией
- Адаптивная верстка
- Интеграция с внешними библиотеками
- За основу взят шаблон 'typerite-master' от StyleShout
### Стек
- Django
- PostgreSQL
- Bootstrap
- Pillow
- Markdown
- Pagedown
- Taggit

### Установка   
1. Склонируйте репазиторий:
   ```bash
   git clone https://github.com/Newport911/Website_about_film_photography.git
   ```
2. Зайдите в деррикторию проекта:
   ```bash
   cd film   
   ```                   
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Настройте Postgressql:
   создайте файл с именем .env в корне проекта:
   ```bash
   touch .env
   ```
   После чего заполните его следующими данными:
   ```bash
   DB_NAME=ВАШЕ НАЗВАНИЕ БАЗЫ ДАННЫХ
   DB_USER= ВАШЕ ИМЯ ДЛЯ ДОСТУПАВ БАЗУ ДАННЫХ
   DB_PASSWORD= ВАШ ПАРОЛЬ ДЛЯ ДОСТУПА В БАЗУ ДАННЫХ
   DB_HOST=localhost
   DB_PORT=5432
   ```
5. Создайте миграции в базе данных:
   ```bash
   python manage.py migrate
   ```
   Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```
   Создайте теги BW, Author и Color для статей:
   ```bash
   python manage.py shell
   from django.contrib.auth.models import User
   from taggit.models import Tag
   Tag.objects.get_or_create(name='BW')
   Tag.objects.get_or_create(name='Author')
   Tag.objects.get_or_create(name='Color')
   ```
5. Запустите сервер для локальной разработки:
   ```bash
   python manage.py runserver
   ``` 

### Поддержка  
Если у вас возникли какие-либо вопросы или предложения, пожалуйста, пишите на почту: portnovdisk.com    
