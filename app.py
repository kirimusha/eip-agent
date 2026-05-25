import os
import time
import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent
from langchain.agents.agent import AgentExecutor
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434/v1")

MODELS = {
    "qwen2.5:3b": {"label": "Qwen 2.5", "size": "3B"},
}

search_tool = DuckDuckGoSearchResults(
    name="web_search",
    description="Поиск актуальной информации в интернете"
)

@tool
def calculator(expression: str) -> str:
    """Вычисляет математические выражения"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Ошибка: {e}"

TOOLS = [search_tool, calculator]
SYSTEM_PROMPT = (
    "Ты — умный ИИ-ассистент. Отвечай точно и по существу. "
    "Используй web_search для актуальных данных, calculator для вычислений."
)

def build_agent(model: str) -> AgentExecutor:
    llm = ChatOpenAI(
        model=model,
        temperature=0.3,
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_openai_tools_agent(llm, TOOLS, prompt)
    return AgentExecutor(agent=agent, tools=TOOLS, verbose=True)


@cl.on_chat_start
async def start_chat():
    default_model = list(MODELS.keys())[0]
    cl.user_session.set("model", default_model)
    cl.user_session.set("agent_executor", build_agent(default_model))
    cl.user_session.set("chat_history", [])

    info = MODELS[default_model]
    await cl.Message(
        content=f"Привет! Я ИИ-ассистент.\n\nМодель: {info['label']} {info['size']}\nИнструменты: поиск в интернете, калькулятор\n\nНапиши свой вопрос."
    ).send()


@cl.on_message
async def main(message: cl.Message):
    agent_executor = cl.user_session.get("agent_executor")
    model = cl.user_session.get("model")
    chat_history = cl.user_session.get("chat_history")

    start_time = time.time()
    msg = cl.Message(content="Думаю...")
    await msg.send()

    try:
        response = await cl.make_async(agent_executor.invoke)({
            "input": message.content,
            "chat_history": chat_history,
        })
        
        elapsed = time.time() - start_time
        output = response["output"]
        info = MODELS[model]

        msg.content = (
            f"{output}\n\n"
            f"---\n"
            f"Время: {elapsed:.1f}s · Модель: {info['label']} {info['size']}"
        )
        await msg.update()

        chat_history.append(("human", message.content))
        chat_history.append(("ai", output))
        cl.user_session.set("chat_history", chat_history)
        
    except Exception as e:
        error_msg = f"Ошибка: {str(e)}"
        msg.content = error_msg
        await msg.update()