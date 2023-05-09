# Документация CRM-фитнес платформы с телеграм-ботом.

Проект основан на фреймворке **Django** и включает в себя два основных 
сервиса: веб-приложение и телеграм-бот на базе фреймворка **aiogram**. Взаимодействие между сервисами осуществляется через DRF. 

>Так как проект небольшой и команда состоит из 5 человек,
для большой эффективности использовали метод **Agile**.

Ниже перечисленные инструменты обладают большим преимуществом, 
поэтому проект разворачивали с их использованием.
+ **Docker** позволяет упаковывать приложение в контейнер, который легко запускать на любой платформе. 
+ **Docker Compose** позволяет запускать и управлять 
несколькими контейнерами, включая контейнеры для приложения, базы данных и других зависимостей, 
как единое приложение. 
+ Poetry создает виртуальное окружение для каждого проекта, соответственно позволяет избегать 
конфликтов между разными сервисами и автоматически создает файл "pyproject.toml". 



CRM построен на основе архитектурного паттерна **MVC (Model-View-Controller)**. 
В проекте есть следующие модели: ```Client, Payment, LazyDays, 
Training, Coach, Group, GroupTraining.``` Часто повторяющиеся поля в моделях вынесены в абстрактную 
модель `CreatedAndUpdatedTime`. Для удобной визуализации моделей и 
связей между ними с использованием плагина `Diagrams.net Integration` реализована схема.
Для большинства моделей использован стандартный `CRUD`. Отличается логика 
продлевание абонемента,  заложена в создании новой оплаты в `PaymentCreateView`. Имеется стандартная логинка.

Так же для удобного получения активных клиентов реализован объектный менеджер`ActiveClientManager`. 
Функция `active_clients`: возвращает активных клиентов 
(клиенты у которых есть заморозка, активными не считаются). Функция `active_payment` принимает 
`client.id` и возвращает активный платеж на данный момент. Используется при осуществлении 
заморозки абонемента.

На главной странице реализован фильтр с использованием библиотеки `django_filters`, который по умолчанию возвращает 
всех клиентов. Так же может возвращать активных и не активных клиентов. 

Так как **DRF** является удобной надстройкой над **Django** его использование 
является оптимальным. API защищены **TOKEN**-ом и хранится в .env файле.

Телеграм-бот построен на базе фреймворка aiogram и взаимодействует с веб-приложением через API, 
отправляет запросы к API веб-приложения для получения и отправки данных.
Бот предоставляет пользователям возможность регистрироваться, отправлять личные данные, 
получать приглашения на тренировку и  рассылки. Рассылку можно делать активным клиентам, 
всем клиентам, а так же по группам. Из телегарм-бота можно отправить приглашение 
на тренировку клиентам. Так же выбора тренера является гибким. 
Что бы управлять  администраторскими возможностями из телеграм, необходимо в **Django** админ панели в конфигурациях добавить
телеграм-id. Для того чтоб уменшить нагрузку на сервер, используется библиотека **constance**, для хранения кеша.
    
При отправке приглашения на тренировку в последующем отправляется ссылка на само занятие. Для передачи ссылки из 
одного сервера на другой используем библиотеку `redis`.

Статические изменяемые части кода написаны на языке`Java Script` с использованием  
`AJAX`-запросов. Также при реализации заморозки при помощи `API`,  `TOKEN`  был сохранен в 
`config.js`. Для реализации статистики использовалась библиотека `Chart JS`.

Для быстрого выявления ошибок в коде и устранение их на ранних этапах разработки,
были написаны `Юнит-тесты`.
Так же были написаны приемочные тесты с использованием библиотеки `Selenium`

>В результате разработки CRM-фитнес платформы с телеграм-ботом были достигнуты 
поставленные цели и решены задачи. Платформа предоставляет пользователям удобный и 
гибкий функционал, позволяющий легко управлять платформой.

>В целом, проект достаточно сложный, но благодаря правильной организации процессов
разработки и использованию современных технологий удалось достичь хорошего результата.