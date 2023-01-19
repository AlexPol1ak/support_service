# Suport service
Сервис позволяющий зарегистрированным пользователям оставлять обращения в службу поддержки.<br>
Агенты отслеживают открытые/закрытые обращения, отвечают на обращения, правляют их статусом.<br>
Пользователь может комментировать ответы, агенты отвечать на комментарии.Уведомления об ответах и изменениях статуса обращения отправляются на email пользователю.<br>
Администратор обладает всем функционалом агента поддержки, а также может назначать и разжаловать агентов поддержки из числа зарегистрированных пользователей.
<br>
<br>
<h3>
 Запуск приложения.
</h3>
Запуск приложения осуществляется в docker (docker-compose up). Перед запуском необходимо передать переменные окружения с конфигурацией (примерный файл .env).<br>
После старта будут запущены следующие контейнеры: База данных (Postgres:15), pgAdmin4, redis, flower, nginx , web (api).<br>
<br>
Документация по API будет доступна по следубщим маршрутам:<br>
1. /api/doc/schema/<br>
2. /api/doc/schema/swagger/<br>
3. /api/doc/schema/redoc/<br>
<br>
