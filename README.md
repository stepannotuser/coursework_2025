# coursework_2025

Курсовой проект: активное обучение автомата сетевого сервиса  
(Tomsk State University, 2025)

использую [AALpy](https://github.com/DES-Lab/AALpy) - открытую библиотеку активного обучения автоматов на Python.

установка зависимостей:
1) pip install aalpy

Сборка проекта через Makefile:
1) make full

или:

1) python3 src/booking_server.py & запуск сервера (python3 src/turnstile_server.py & для запуска альтернативного сервера)
2) python3 src/proxy.py & запуск прокси
3) python3 src/extract_alphabet.py извлечение алфавита
4) python3 src/fsm_learner.py запуск fsm learning и выгрузка результата
