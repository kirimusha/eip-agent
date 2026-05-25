FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    "chainlit==2.5.5" \
    "langchain==0.2.17" \
    "langchain-core==0.2.43" \
    "langchain-openai==0.1.25" \
    "langchain-community==0.2.19" \
    "duckduckgo-search==6.4.2"

COPY app.py /app/app.py

CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]