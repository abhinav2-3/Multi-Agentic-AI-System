# from src.pipelines.pipeline import run_research_pipeline
# from src.tools.tools import scrape_url, web_search

# # search = web_search("Price hikes of phones, laptop, when it will saturate")
# # search = scrape_url(
# #     "https://www.buysellram.com/blog/memory-prices-expected-to-surge-again-in-q1-2026-putting-global-device-makers-under-severe-cost-pressure/"
# # )
# # print(search)


# result = run_research_pipeline("What is the Impact of AI on job 2026")
# print(result)


from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=SecretStr(os.getenv("GROQ_API_KEY") or ""),
)


class SupportState(TypedDict):
    query: str
    category: str
    resolution: str
    final_response: str


def classifier_agent(state: SupportState) -> SupportState:
    messages: list[SystemMessage | HumanMessage] = [
        SystemMessage(
            content="Classify the query into one of: billing, technical, general. Reply with only the category word."
        ),
        HumanMessage(content=state["query"]),
    ]
    result = llm.invoke(messages)
    state["category"] = str(result.content).strip().lower()
    return state


def resolver_agent(state: SupportState) -> SupportState:
    messages: list[SystemMessage | HumanMessage] = [
        SystemMessage(
            content=f"You are a {state['category']} support expert. Resolve the issue concisely."
        ),
        HumanMessage(content=state["query"]),
    ]
    result = llm.invoke(messages)
    state["resolution"] = str(result.content).strip()
    return state


def responder_agent(state: SupportState) -> SupportState:
    messages: list[SystemMessage | HumanMessage] = [
        SystemMessage(content="Write a polished, friendly customer support reply."),
        HumanMessage(
            content=f"Query: {state['query']}\nResolution: {state['resolution']}"
        ),
    ]
    result = llm.invoke(messages)
    state["final_response"] = str(result.content).strip()
    return state


graph = StateGraph(SupportState)

graph.add_node("classifier", classifier_agent)
graph.add_node("resolver", resolver_agent)
graph.add_node("responder", responder_agent)

graph.set_entry_point("classifier")
graph.add_edge("classifier", "resolver")
graph.add_edge("resolver", "responder")
graph.add_edge("responder", END)

app = graph.compile()

result = app.invoke(
    {
        "query": "I can't login to my account, it says invalid password but I just reset it",
        "category": "",
        "resolution": "",
        "final_response": "",
    }
)

print("Category:", result["category"])
print("Resolution:", result["resolution"])
print("Final Response:", result["final_response"])
