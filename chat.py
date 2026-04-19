import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END, MessagesState

load_dotenv('.env')

qwen_token = os.getenv('QWEN_TOKEN')

llm = ChatOpenAI(
    model="qwen3.5-plus",
    api_key=qwen_token,
    streaming=True,
    base_url="https://qwen.aikit.club/v1/",
    temperature=0.7,
)

def chatbot(state: MessagesState):
    response = llm.invoke(state['messages'])
    return {'messages' : response}


graph_builder = StateGraph(MessagesState)

graph_builder.add_node('chatbot', chatbot)
graph_builder.add_edge(START, 'chatbot')
graph_builder.add_edge('chatbot', END)

memory=MemorySaver()
agent = graph_builder.compile(checkpointer=memory)


def run_chat():
    print("Чат запущен! (Для выхода введите :q)")
    config = {"configurable": {"thread_id": "session_1"}}

    while True:
        user_input = input("\nВы: ")
        if len(user_input) == 0 or user_input.isspace():
            continue
        if user_input.lower() == ":q":
            break

        print("Qwen: ", end="", flush=True)

        events = agent.stream(
            {"messages": [HumanMessage(user_input)]},
            config,
            stream_mode="messages"
        )

        for chunk, metadata in events:
            if metadata.get("langgraph_node") == "chatbot":
                if chunk.content:
                    print(chunk.content, end="", flush=True)

        print("")


if __name__ == "__main__":
    run_chat()



