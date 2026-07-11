# eip-agent

<img width="1512" height="916" alt="image" src="https://github.com/user-attachments/assets/2eded2a1-8855-4661-83ec-b50bcdbf4dd5" />

<img width="1280" height="775" alt="telegram-cloud-photo-size-2-5235959596965370646-y" src="https://github.com/user-attachments/assets/eff36294-dd8b-4ad7-a83b-396a88c910df" />

<img width="1280" height="813" alt="telegram-cloud-photo-size-2-5233388745506101361-y" src="https://github.com/user-attachments/assets/95355ec4-c442-47cf-925f-d1bfb5ed3172" />

<div align="center">

**ИИ-ассистент с локальным запуском на базе Qwen 2.5, LangChain и Chainlit**

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Chainlit](https://img.shields.io/badge/Chainlit-2.5.5-orange)
![LangChain](https://img.shields.io/badge/LangChain-0.2.17-1C3C3C)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 📖 Описание

**EIP Agent** — веб-приложение с ИИ-агентом, полностью работающим на локальном оборудовании без обращения к внешним LLM-провайдерам. Модель **Qwen 2.5** запускается через **Ollama**, агент построен на **LangChain**, а интерфейс чата реализован с помощью **Chainlit**. Всё разворачивается одной командой через Docker Compose.

Агент умеет искать актуальную информацию в интернете и выполнять вычисления, сохраняя историю диалога в рамках сессии.

## 📸 Скриншоты

<div align="center">
<img width="800" alt="Интерфейс EIP Agent" src="https://github.com/user-attachments/assets/2eded2a1-8855-4661-83ec-b50bcdbf4dd5" />
<br/><br/>
<img width="400" alt="Пример диалога 1" src="https://github.com/user-attachments/assets/eff36294-dd8b-4ad7-a83b-396a88c910df" />
<img width="400" alt="Пример диалога 2" src="https://github.com/user-attachments/assets/95355ec4-c442-47cf-925f-d1bfb5ed3172" />
</div>

## ✨ Возможности

- 💬 Чат-интерфейс на базе Chainlit с отображением времени генерации ответа
- 🔍 Поиск актуальной информации в интернете (DuckDuckGo)
- 🧮 Вычисление математических выражений
- 🧠 Локальная LLM-модель Qwen 2.5 (7B) через Ollama — без внешних API и передачи данных наружу
- 🐳 Полностью контейнеризированное развёртывание через Docker Compose
- 📊 Презентация архитектуры проекта (`presentation.html`)

## 🏗️ Архитектура

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────┐
│   Браузер   │◄────►│  web-agent       │◄────►│   Ollama    │
│  (Chainlit) │      │ (Chainlit +      │      │ (Qwen 2.5)  │
│             │      │  LangChain agent)│      │             │
└─────────────┘      └──────────────────┘      └─────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │  Инструменты:    │
                     │  • web_search    │
                     │  • calculator    │
                     └──────────────────┘
```

Сервис `ollama-init` при первом запуске автоматически скачивает модель `qwen2.5:7b` в контейнер Ollama.

## 🛠️ Технологический стек

| Компонент | Технология |
|---|---|
| Язык | Python 3.11 |
| LLM-модель | Qwen 2.5 (через Ollama) |
| Агентный фреймворк | LangChain (`create_openai_tools_agent`) |
| UI / чат | Chainlit |
| Поиск | DuckDuckGo Search |
| Контейнеризация | Docker, Docker Compose |

## 📁 Структура проекта

```
eip-agent/
├── app.py                # Логика агента: инструменты, промпт, обработчики Chainlit
├── chainlit.md            # Приветственный экран Chainlit
├── Dockerfile              # Образ приложения
├── docker-compose.yml      # Оркестрация: Ollama + инициализация модели + агент
├── requirements.txt        # Python-зависимости
├── presentation.html       # Презентация архитектуры проекта
└── public/
    └── style.css            # Кастомные стили интерфейса
```

## 🚀 Быстрый старт

### Требования

- Docker и Docker Compose
- ~8 ГБ свободного места под модель `qwen2.5:7b`

### Запуск

```bash
git clone https://github.com/kirimusha/eip-agent.git
cd eip-agent
docker compose up --build
```

При первом запуске сервис `ollama-init` дождётся готовности Ollama и автоматически скачает модель `qwen2.5:7b`. Это может занять несколько минут в зависимости от скорости интернета.

После запуска интерфейс будет доступен по адресу:

```
http://localhost:8000
```

### Остановка

```bash
docker compose down
```

Чтобы удалить и скачанную модель Ollama:

```bash
docker compose down -v
```

## ⚙️ Переменные окружения

| Переменная | Значение по умолчанию | Описание |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://ollama:11434/v1` | Адрес OpenAI-совместимого API Ollama |
| `OLLAMA_MODEL` | `qwen2.5:7b` | Модель, используемая агентом |

## 🧩 Инструменты агента

- **web_search** — поиск актуальной информации в интернете через DuckDuckGo
- **calculator** — безопасное вычисление математических выражений

## 📄 Лицензия

Проект распространяется под лицензией [MIT](LICENSE).
