Запуск приложение доступен в двух формах: на одном компьютере и клиент и сервер И сервер на докере, а клиент на основной машине.

Первый вариант установки.
1. Установить на компьютер версию интерпретатора языка программирования python версии не ниже 3.10. С процессом установки
можно ознакомиться по ссылке https://realpython.com/installing-python/
2. Необходимо установить pip(система управления пакетами для python). С процессом его установки под различные операционные 
системы можно так же ознакомиться по следующей ссылке: https://pip.pypa.io/en/stable/installation/
3. Далее необходимо произвести установку зависимостей для корректной работы приложения, делается это в командной строке
операционной системы с помощью команды pip3 install -r requirements.txt
4. Следующим шагом, после устновки всех зависимостей, и у клиента и у сервера необходимо установить переменные окружения.
В *nix операционных системах это делается через команду export. Необходимо ввести:
export ENV HASH_SALT=9fc47da85894433819877a9d0e3f01f6ff35afeb25cc6058d138284abd3a050b
export ENV SECRET=etg64vtah7r6atw74afiar6jtw4rsetrset69c8s
Для операционной системы под управлением Windows предлагается ознакомиться с материалом по ссылке: https://learn.microsoft.com/ru-ru/sql/integration-services/lesson-1-1-creating-working-folders-and-environment-variables?view=sql-server-ver16
5. Далее запускаем приложение коммандой python3.10 main.py
6. И, чтобы начать работать с приложением, запускаем клиент, в другом окне коммандой строки, с помощью комманды python3.10 client.py

Второй вариант устнаовки.
Для этого необходимо повторить все шаги с первого варианта установки до 4-ого. 
1. Запустите приложение Docker(подразумевается, что у пользователя уже установлен клиент данного приложение, если нет, то 
с процессом установки можно ознакомиться в интернете) и введите следующую комманду: docker build -t flask .(точка часть комманды)
2. Произведите запуск собранного образа с помощью комманды: docker run -d -p 5000:5000 flask
3. Произведите подключение к серверу через клиент запустив его на основной машине с помощью комманды: python3.10 client.py