README файл с инструкциями по запуску и использованию API.

В проект добавлен докер компоуз, поэтому проект запускается без какой-либо мороки.

1. Переходим в папку /dev_tools/ проекта через терминал.
2. Прописываем в терминал docker compose up --build (при недостатке прав, возможно потребуется добавить sudo перед командой)
3. Ждем пока контейнер развернется. При возникновении каких-то проблем с докером (у меня всё работает, но бывает проблема с локальными конфигурациями), пишем мне @Forzzy, я помогаю.
4. Заходим на localhost:8000/docs для получения документации.
5. Пользуемся!

Я постарался максимально понятно структурировать сваггер (localhost:8000/docs), дабы вопросов возникнуть не могло. Потому не вижу смысла здесь дублировать все эндпоинты. Однако ж всё по тз.
Тесты делать не стал, ибо и так постарался приложить максимально усилий к вашему ТЗ, поэтому извините)

Жду обратной связи, спасибо!