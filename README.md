Посмотреть на работу сайта можно по ссылке: http://178.154.194.230/

Пользователи для тестирования:

1. login: admin  password: admin
2. login: user2  password: 1234

Для авторизации используется расширенная модель пользователя с полями is_administrator (дает право просмотра и редактирования всех заявок и клиентов) и is_employee (дает право просмотра собственных заявок и изменения статуса их выполнения). Данные поля может устанавливать Django администратор в админке.

Логика поиска реализована в crm/services/search_in_applications.py  
