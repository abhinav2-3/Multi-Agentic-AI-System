from typing import Annotated, Literal, TypedDict
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, StateGraph, END, add_messages
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, SecretStr
from rich import print
from langgraph.checkpoint.memory import MemorySaver

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
    messages: Annotated[list[BaseMessage], add_messages]
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
    system_note = SystemMessage(
        content="You are a friendly AI assistant. Respond naturally and concisely, using the conversation history for context."
    )

    output = llm.invoke([system_note] + state["messages"]).content
    return {"chat_reply": output}


def process_question(state: AssistantState):
    system_note = SystemMessage(
        content="You are an expert AI assistant. Answer accurately using conversation history for context. If uncertain, say so."
    )
    output = llm.invoke([system_note] + state["messages"]).content
    return {"question_answer": output}


def process_search(state: AssistantState):
    system_note = SystemMessage(
        content="Pretend you are a web search tool. Respond with: 'This would trigger a web search for: <query>'"
    )
    output = llm.invoke([system_note] + state["messages"]).content
    return {"search_result": output}


def format_output(state: AssistantState):
    if state["tone"] == "chitchat":
        response = state["chat_reply"]

    elif state["tone"] == "question":
        response = state["question_answer"]

    else:
        response = state["search_result"]

    return {"final_response": response, "messages": [AIMessage(content=response)]}


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

checkpointer = MemorySaver()
workflow = graph.compile(checkpointer=checkpointer)

# config: RunnableConfig = {"configurable": {"thread_id": "user-1"}}

# while True:
#     user_input = input("Type here: ")
#     print("User: ", user_input)
#     result = workflow.invoke(
#         {"input": user_input, "messages": [HumanMessage(content=user_input)]},
#         config=config,
#     )
#     print("AI: ", result["messages"][-1].content)
