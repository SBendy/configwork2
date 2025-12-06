# configproj2

CLI-инструмент для анализа и визуализации графа зависимостей пакетов JavaScript (npm),
реализованный на Python **без использования менеджеров пакетов и сторонних библиотек
для получения зависимостей**.

Проект выполнен в рамках учебного задания и реализует поэтапно:
- конфигурируемое CLI-приложение,
- сбор данных о зависимостях npm-пакетов,
- построение графа зависимостей (включая транзитивные),
- обработку циклов,
- поиск обратных зависимостей,
- визуализацию зависимостей в текстовом виде (ASCII-дерево) и в формате D2.

---

## Возможности

- Разбор параметров командной строки
- Проверка корректности входных параметров
- Получение прямых зависимостей npm-пакета по заданной версии
- Построение графа зависимостей с учетом транзитивности
- Нерекурсивный DFS с ограничением глубины
- Корректная обработка циклических зависимостей
- Режим тестирования с искусственным репозиторием
- Поиск обратных зависимостей
- Визуализация:
  - ASCII-дерево
  - экспорт графа в язык диаграмм D2

---

## Требования

- Python 3.10+
- Доступ в интернет (только для режима `real`)

Дополнительные библиотеки **не требуются**.

---

## Установка и использование

```bash
git clone https://github.com/<your-username>/configproj2.git
cd configproj2
```

---

## Использование

```Вводится конфигурация для запуска,пример конфигурации:
-n A -r test_repo.txt -m test -v 1.0.0 -d 5 -a --reverse --d2

| Параметр    | За что отвечает       | Когда менять        |
| ----------- | --------------------- | ------------------- |
| `-n`        | Корневой пакет        | Другой пакет        |
| `-r`        | Источник зависимостей | Другой файл/URL     |
| `-m`        | Режим работы          | test ↔ real         |
| `-v`        | Версия пакета         | Другая версия       |
| `-d`        | Глубина анализа       | Сложность графа     |
| `-a`        | ASCII-дерево          | Нужна визуализация  |
| `--reverse` | Обратные зависимости  | Анализ влияния      |
| `--d2`      | D2-формат             | Построение диаграмм |
```
---

## Пример работы

```Конфигурация:
package_name=A
repo=test_repo.txt
mode=test
version=1.0.0
ascii_tree=True
max_depth=5
reverse=True
d2=True

Прямые зависимости A@1.0.0:
  B@1.0.0
  C@1.0.0

Режим обратных зависимостей для A@1.0.0
Пакеты, зависящие от него:
  D@1.0.0
  C@1.0.0
  B@1.0.0

ASCII-дерево обратных зависимостей:
A@1.0.0
└─ D@1.0.0
   └─ C@1.0.0
      ├─ A@1.0.0 (*)
      └─ B@1.0.0
         └─ A@1.0.0 (*)

Циклы (в графе обратных зависимостей):
  A@1.0.0 -> D@1.0.0 -> C@1.0.0 -> A@1.0.0
  A@1.0.0 -> D@1.0.0 -> C@1.0.0 -> B@1.0.0 -> A@1.0.0

--- D2 описание графа ---
"A@1.0.0"
"B@1.0.0"
"C@1.0.0"
"D@1.0.0"
"A@1.0.0" -> "B@1.0.0"
"A@1.0.0" -> "C@1.0.0"
"B@1.0.0" -> "C@1.0.0"
"C@1.0.0" -> "D@1.0.0"
"D@1.0.0" -> "A@1.0.0"


Process finished with exit code 0

Пример с реальной библиотекой

main.py -n express -r https://github.com/expressjs/express -m real -v 4.18.2 -d 2 -a --d2 
Конфигурация:
package_name=express
repo=https://github.com/expressjs/express
mode=real
version=4.18.2
ascii_tree=True
max_depth=2
reverse=False
d2=True

[debug] Fetching: https://registry.npmjs.org/express/4.18.2
[debug] Fetching: https://registry.npmjs.org/content-disposition/0.5.4
[debug] Fetching: https://registry.npmjs.org/merge-descriptors/1.0.1
[debug] Fetching: https://registry.npmjs.org/cookie-signature/1.0.6
[debug] Fetching: https://registry.npmjs.org/setprototypeof/1.2.0
[debug] Fetching: https://registry.npmjs.org/path-to-regexp/0.1.7
[debug] Fetching: https://registry.npmjs.org/array-flatten/1.1.1
[debug] Fetching: https://registry.npmjs.org/serve-static/1.15.0
[debug] Fetching: https://registry.npmjs.org/range-parser/latest
[debug] Fetching: https://registry.npmjs.org/finalhandler/1.2.0
[debug] Fetching: https://registry.npmjs.org/content-type/latest
[debug] Fetching: https://registry.npmjs.org/utils-merge/1.0.1
[debug] Fetching: https://registry.npmjs.org/http-errors/2.0.0
[debug] Fetching: https://registry.npmjs.org/body-parser/1.20.1
[debug] Fetching: https://registry.npmjs.org/proxy-addr/latest
[debug] Fetching: https://registry.npmjs.org/methods/latest
[debug] Fetching: https://registry.npmjs.org/accepts/latest
[debug] Fetching: https://registry.npmjs.org/cookie/0.5.0
[debug] Fetching: https://registry.npmjs.org/fresh/0.5.2
[debug] Fetching: https://registry.npmjs.org/vary/latest
[debug] Fetching: https://registry.npmjs.org/etag/latest
Прямые зависимости express@4.18.2:
  qs@6.11.0
  depd@2.0.0
  etag@~1.8.1
  send@0.18.0
  vary@~1.1.2
  debug@2.6.9
  fresh@0.5.2
  cookie@0.5.0
  accepts@~1.3.8
  methods@~1.1.2
  type-is@~1.6.18
  parseurl@~1.3.3
  statuses@2.0.1
  encodeurl@~1.0.2
  proxy-addr@~2.0.7
  body-parser@1.20.1
  escape-html@~1.0.3
  http-errors@2.0.0
  on-finished@2.4.1
  safe-buffer@5.2.1
  utils-merge@1.0.1
  content-type@~1.0.4
  finalhandler@1.2.0
  range-parser@~1.2.1
  serve-static@1.15.0
  array-flatten@1.1.1
  path-to-regexp@0.1.7
  setprototypeof@1.2.0
  cookie-signature@1.0.6
  merge-descriptors@1.0.1
  content-disposition@0.5.4

Обход графа зависимостей (DFS) от express@4.18.2, глубина <= 2
Порядок обхода:
  express@4.18.2
  content-disposition@0.5.4
  safe-buffer@5.2.1
  merge-descriptors@1.0.1
  cookie-signature@1.0.6
  setprototypeof@1.2.0
  path-to-regexp@0.1.7
  array-flatten@1.1.1
  serve-static@1.15.0
  escape-html@~1.0.3
  encodeurl@~1.0.2
  parseurl@~1.3.3
  send@0.18.0
  range-parser@~1.2.1
  finalhandler@1.2.0
  on-finished@2.4.1
  statuses@2.0.1
  unpipe@~1.0.0
  debug@2.6.9
  content-type@~1.0.4
  utils-merge@1.0.1
  http-errors@2.0.0
  toidentifier@1.0.1
  inherits@2.0.4
  depd@2.0.0
  body-parser@1.20.1
  iconv-lite@0.4.24
  raw-body@2.5.1
  type-is@~1.6.18
  destroy@1.2.0
  unpipe@1.0.0
  bytes@3.1.2
  qs@6.11.0
  proxy-addr@~2.0.7
  ipaddr.js@1.9.1
  forwarded@0.2.0
  methods@~1.1.2
  accepts@~1.3.8
  negotiator@0.6.3
  mime-types@~2.1.34
  cookie@0.5.0
  fresh@0.5.2
  vary@~1.1.2
  etag@~1.8.1

Циклы не обнаружены.

ASCII-дерево зависимостей:
express@4.18.2
├─ qs@6.11.0
├─ depd@2.0.0
├─ etag@~1.8.1
├─ send@0.18.0
├─ vary@~1.1.2
├─ debug@2.6.9
├─ fresh@0.5.2
├─ cookie@0.5.0
├─ accepts@~1.3.8
│  ├─ mime-types@~2.1.34
│  └─ negotiator@0.6.3
├─ methods@~1.1.2
├─ type-is@~1.6.18
├─ parseurl@~1.3.3
├─ statuses@2.0.1
├─ encodeurl@~1.0.2
├─ proxy-addr@~2.0.7
│  ├─ forwarded@0.2.0
│  └─ ipaddr.js@1.9.1
├─ body-parser@1.20.1
│  ├─ qs@6.11.0 (*)
│  ├─ depd@2.0.0 (*)
│  ├─ bytes@3.1.2
│  ├─ debug@2.6.9 (*)
│  ├─ unpipe@1.0.0
│  ├─ destroy@1.2.0
│  ├─ type-is@~1.6.18 (*)
│  ├─ raw-body@2.5.1
│  ├─ iconv-lite@0.4.24
│  ├─ http-errors@2.0.0
│  ├─ on-finished@2.4.1
│  └─ content-type@~1.0.4
├─ escape-html@~1.0.3
├─ http-errors@2.0.0 (*)
├─ on-finished@2.4.1 (*)
├─ safe-buffer@5.2.1
├─ utils-merge@1.0.1
├─ content-type@~1.0.4 (*)
├─ finalhandler@1.2.0
│  ├─ debug@2.6.9 (*)
│  ├─ unpipe@~1.0.0
│  ├─ parseurl@~1.3.3 (*)
│  ├─ statuses@2.0.1 (*)
│  ├─ encodeurl@~1.0.2 (*)
│  ├─ escape-html@~1.0.3 (*)
│  └─ on-finished@2.4.1 (*)
├─ range-parser@~1.2.1
├─ serve-static@1.15.0
│  ├─ send@0.18.0 (*)
│  ├─ parseurl@~1.3.3 (*)
│  ├─ encodeurl@~1.0.2 (*)
│  └─ escape-html@~1.0.3 (*)
├─ array-flatten@1.1.1
├─ path-to-regexp@0.1.7
├─ setprototypeof@1.2.0
├─ cookie-signature@1.0.6
├─ merge-descriptors@1.0.1
└─ content-disposition@0.5.4
   └─ safe-buffer@5.2.1 (*)

--- D2 описание графа ---
"express@4.18.2"
"qs@6.11.0"
"depd@2.0.0"
"etag@~1.8.1"
"send@0.18.0"
"vary@~1.1.2"
"debug@2.6.9"
"fresh@0.5.2"
"cookie@0.5.0"
"accepts@~1.3.8"
"methods@~1.1.2"
"type-is@~1.6.18"
"parseurl@~1.3.3"
"statuses@2.0.1"
"encodeurl@~1.0.2"
"proxy-addr@~2.0.7"
"body-parser@1.20.1"
"escape-html@~1.0.3"
"http-errors@2.0.0"
"on-finished@2.4.1"
"safe-buffer@5.2.1"
"utils-merge@1.0.1"
"content-type@~1.0.4"
"finalhandler@1.2.0"
"range-parser@~1.2.1"
"serve-static@1.15.0"
"array-flatten@1.1.1"
"path-to-regexp@0.1.7"
"setprototypeof@1.2.0"
"cookie-signature@1.0.6"
"merge-descriptors@1.0.1"
"content-disposition@0.5.4"
"unpipe@~1.0.0"
"inherits@2.0.4"
"toidentifier@1.0.1"
"bytes@3.1.2"
"unpipe@1.0.0"
"destroy@1.2.0"
"raw-body@2.5.1"
"iconv-lite@0.4.24"
"forwarded@0.2.0"
"ipaddr.js@1.9.1"
"mime-types@~2.1.34"
"negotiator@0.6.3"
"express@4.18.2" -> "qs@6.11.0"
"express@4.18.2" -> "depd@2.0.0"
"express@4.18.2" -> "etag@~1.8.1"
"express@4.18.2" -> "send@0.18.0"
"express@4.18.2" -> "vary@~1.1.2"
"express@4.18.2" -> "debug@2.6.9"
"express@4.18.2" -> "fresh@0.5.2"
"express@4.18.2" -> "cookie@0.5.0"
"express@4.18.2" -> "accepts@~1.3.8"
"express@4.18.2" -> "methods@~1.1.2"
"express@4.18.2" -> "type-is@~1.6.18"
"express@4.18.2" -> "parseurl@~1.3.3"
"express@4.18.2" -> "statuses@2.0.1"
"express@4.18.2" -> "encodeurl@~1.0.2"
"express@4.18.2" -> "proxy-addr@~2.0.7"
"express@4.18.2" -> "body-parser@1.20.1"
"express@4.18.2" -> "escape-html@~1.0.3"
"express@4.18.2" -> "http-errors@2.0.0"
"express@4.18.2" -> "on-finished@2.4.1"
"express@4.18.2" -> "safe-buffer@5.2.1"
"express@4.18.2" -> "utils-merge@1.0.1"
"express@4.18.2" -> "content-type@~1.0.4"
"express@4.18.2" -> "finalhandler@1.2.0"
"express@4.18.2" -> "range-parser@~1.2.1"
"express@4.18.2" -> "serve-static@1.15.0"
"express@4.18.2" -> "array-flatten@1.1.1"
"express@4.18.2" -> "path-to-regexp@0.1.7"
"express@4.18.2" -> "setprototypeof@1.2.0"
"express@4.18.2" -> "cookie-signature@1.0.6"
"express@4.18.2" -> "merge-descriptors@1.0.1"
"express@4.18.2" -> "content-disposition@0.5.4"
"accepts@~1.3.8" -> "mime-types@~2.1.34"
"accepts@~1.3.8" -> "negotiator@0.6.3"
"proxy-addr@~2.0.7" -> "forwarded@0.2.0"
"proxy-addr@~2.0.7" -> "ipaddr.js@1.9.1"
"body-parser@1.20.1" -> "qs@6.11.0"
"body-parser@1.20.1" -> "depd@2.0.0"
"body-parser@1.20.1" -> "bytes@3.1.2"
"body-parser@1.20.1" -> "debug@2.6.9"
"body-parser@1.20.1" -> "unpipe@1.0.0"
"body-parser@1.20.1" -> "destroy@1.2.0"
"body-parser@1.20.1" -> "type-is@~1.6.18"
"body-parser@1.20.1" -> "raw-body@2.5.1"
"body-parser@1.20.1" -> "iconv-lite@0.4.24"
"body-parser@1.20.1" -> "http-errors@2.0.0"
"body-parser@1.20.1" -> "on-finished@2.4.1"
"body-parser@1.20.1" -> "content-type@~1.0.4"
"http-errors@2.0.0" -> "depd@2.0.0"
"http-errors@2.0.0" -> "inherits@2.0.4"
"http-errors@2.0.0" -> "statuses@2.0.1"
"http-errors@2.0.0" -> "toidentifier@1.0.1"
"http-errors@2.0.0" -> "setprototypeof@1.2.0"
"finalhandler@1.2.0" -> "debug@2.6.9"
"finalhandler@1.2.0" -> "unpipe@~1.0.0"
"finalhandler@1.2.0" -> "parseurl@~1.3.3"
"finalhandler@1.2.0" -> "statuses@2.0.1"
"finalhandler@1.2.0" -> "encodeurl@~1.0.2"
"finalhandler@1.2.0" -> "escape-html@~1.0.3"
"finalhandler@1.2.0" -> "on-finished@2.4.1"
"serve-static@1.15.0" -> "send@0.18.0"
"serve-static@1.15.0" -> "parseurl@~1.3.3"
"serve-static@1.15.0" -> "encodeurl@~1.0.2"
"serve-static@1.15.0" -> "escape-html@~1.0.3"
"content-disposition@0.5.4" -> "safe-buffer@5.2.1"


Process finished with exit code 0
```

<img width="10082" height="957" alt="d2" src="https://github.com/user-attachments/assets/77d85dae-e297-4e78-b721-b3944d68d697" />


