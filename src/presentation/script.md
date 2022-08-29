## 2.1. План демонстрации

Слайд 1 Приветствие
Добрый день мы, команда We want to work in Sber за дни хакатона разработали бота для бронирования объектов в школе 21. Наш бот называется bookbot21_official_bot. Он запущен и вы можете в любой момент перейти по QR коду и посмотреть как он работает. Данная презентация у вас будет доступна по ссылке https://docs.google.com/presentation/d/1CtQpAuedWUlZnD7piRMBZonn19Xd7Shpn8VmeRIwP1k/edit#slide=id.g14632c58c52_2_72
Слайд 2
В настоящее время в Школе 21 бронирование переговорок, спортивного инвентаря и настольных игр происходит “по старинке” в гугл-таблицах. Эта система является устаревшей и неудобной для студентов.
Мы решили автоматизировать процесс бронирования с помощью телеграм бота.
Это удобно, эстетично и самое главное доступно из каждого смартфона
Слайд 3
В настоящем на рынке представлены несколько решений для бронирования помещений, начиная от простейших excel таблиц на локальном компьютере и заканчивая сложными и дорогостоящими решениями. Некоторые из них избыточны для нашей задачи, а другие не имеют функционала разделения ролей. Оптимального готового решения для нашей задачи на рынке не существует.
Слайд 4
Нашей задачей является возможность забронировать объект или помещение.Для бронирования у пользователя должны быть права доступа
Слайд 5
У нас есть роли: абитуриент, студент и сотрудник. И виды объектов бронирования.
На данном слайде видно кто какими правами доступа обладает.
Слайд 6
В ходе разработки мы использовали следующий технологический стек.
Слайд 7
На этом слайде вы видите наш состав команды. У нас было четкое разделение ролей и каждый знал свою задачу.
Слайд 8
Регистрация телеграмм бота
Описание логики работы
Создание баз данных
Взаимодействие с базой данных (запросы, внесение изменений)
Тестирование бота
Оформление
Слайд 9
Мы запустили наш бот на собственном сервере, это позволяет ему быть доступным 24/7
Слайд 10
Интересным решением в нашем проекте было использование фреймворка Django. Это повысило надежность нашего бота + дало возможность в режиме реального времени вносить в базу данных любые объекты и сущности без остановки бота и перезапуска сервера.
Слайд 11
Перед тем  как приступить к разработке бота мы реализовали интерфейс в figma что позволило на этом этапе иметь четкое представление о будущем виде бота.


Слайд 12

Получить обратную связь
Провести нагрузочное тестирование
Составить руководство программиста пользователя
Привлечение бюджета Sber
Реализовать защиту данных и повысить устойчивость бота к неправомерному доступу
Разместить на каждом объекте бронирование QR-код бота
Слайд 13
Сбер за возможность участия в этом соревновании, в котором мы приобрели новые знания и навыки командной работы
Всех пиров в Школе 21 за взаимную поддержку
Организаторов за пиццу