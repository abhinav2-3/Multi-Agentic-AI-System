from typing import Literal, TypedDict
from langgraph.graph import START, StateGraph, END
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, SecretStr
from rich import print

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=SecretStr(os.getenv("GROQ_API_KEY") or ""),
)


# ---------------------------
# Structured Output
# ---------------------------


class ModelStructure(BaseModel):
    processed_input: str = Field(
        description="A clean and formatted version of the user input."
    )

    tone: Literal["chitchat", "question", "search"] = Field(
        description="Intent of the user."
    )


model = llm.with_structured_output(ModelStructure)


# ---------------------------
# Graph State
# ---------------------------


class AssistantState(TypedDict):
    input: str
    processed_input: str
    tone: Literal["chitchat", "question", "search"]
    chat_reply: str
    question_answer: str
    search_result: str
    final_response: str


# ---------------------------
# Agents
# ---------------------------


def process_input(state: AssistantState):
    promptInput = f"""
     You are an input preprocessing assistant.

    Your responsibilities:
    1. Rewrite the user's message into a clean, grammatically correct version without changing its meaning.
    2. Classify the user's intent into exactly one category.

    Categories:
    - chitchat → greetings, casual conversation, jokes, opinions.
    - question → factual questions or requests that can be answered using your knowledge.
    - search → questions requiring recent, live, or external information from the web.

    Return only the structured output.

    User message:
    {state["input"]}
     """

    output = model.invoke(promptInput)
    assert isinstance(output, ModelStructure)
    return {"processed_input": output.processed_input, "tone": output.tone}


def process_chit_chat(state: AssistantState):
    promptInput = f"""
     You are a friendly AI assistant.

    Respond naturally to the user's message.

    Keep the conversation engaging and concise.

    User:
    {state["processed_input"]}
     """

    output = llm.invoke(promptInput).content
    return {"chat_reply": output}


def process_question(state: AssistantState):
    promptInput = f"""
    You are an expert AI assistant.

    Answer the user's question accurately.

    If you are uncertain, clearly say so instead of making up information.

    Question:
    {state["processed_input"]}
     """

    output = llm.invoke(promptInput).content
    return {"question_answer": output}


def process_search(state: AssistantState):
    promptInput = f"""
    Pretend you are a web search tool.

    The following query would normally be sent to a search engine.

    Respond with:
    "This would trigger a web search for: <query>"

    Query:
    {state["processed_input"]}
     """

    output = llm.invoke(promptInput).content
    return {"search_result": output}


def format_output(state: AssistantState):
    if state["tone"] == "chitchat":
        response = state["chat_reply"]

    elif state["tone"] == "question":
        response = state["question_answer"]

    else:
        response = state["search_result"]

    return {"final_response": response}


def classify_tone(
    state: AssistantState,
) -> Literal["chit_chat_node", "question_node", "search_node"]:
    if state["tone"] == "chitchat":
        return "chit_chat_node"
    elif state["tone"] == "question":
        return "question_node"
    else:
        return "search_node"


# ---------------------------
# Graph
# ---------------------------

graph = StateGraph(AssistantState)


# ---------------------------
# Register Nodes
# ---------------------------

graph.add_node("preprocess_node", process_input)

graph.add_node("chit_chat_node", process_chit_chat)

graph.add_node("question_node", process_question)

graph.add_node("search_node", process_search)

graph.add_node("format_output_node", format_output)


# ---------------------------
# Edges
# ---------------------------

graph.add_edge(START, "preprocess_node")


graph.add_conditional_edges("preprocess_node", classify_tone)


graph.add_edge("chit_chat_node", "format_output_node")

graph.add_edge("question_node", "format_output_node")

graph.add_edge("search_node", "format_output_node")


graph.add_edge("format_output_node", END)


# ---------------------------
# Compile
# ---------------------------

workflow = graph.compile()

result = workflow.invoke({"input": "Weather in Delhi today."})

print(result)
