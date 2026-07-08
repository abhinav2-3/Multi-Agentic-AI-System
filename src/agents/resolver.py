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


class ResumeState(TypedDict):
    jd: str
    jd_desc: str
    resume: str
    resolution: str
    final_response: str


def jd_analyzer_agent(state: ResumeState) -> ResumeState:
    messages: list[SystemMessage | HumanMessage] = [
        SystemMessage(
            content="Extract key skills, technologies, experience requirements, and responsibilities from this job description. Be concise and structured."
        ),
        HumanMessage(content=state["jd"]),
    ]
    result = llm.invoke(messages)
    state["jd_desc"] = str(result.content).strip().lower()
    return state


def resume_analyzer_agent(state: ResumeState) -> ResumeState:
    messages: list[SystemMessage | HumanMessage] = [
        SystemMessage(
            content=f"You are a resume expert. Given this JD analysis:\n{state['jd_desc']}\n\nIdentify what matches and what is missing in the resume. Be specific."
        ),
        HumanMessage(content=state["resume"]),
    ]
    result = llm.invoke(messages)
    state["resolution"] = str(result.content).strip()
    return state


def resume_tuning_agent(state: ResumeState) -> ResumeState:
    messages: list[SystemMessage | HumanMessage] = [
        SystemMessage(
            content="You are a LaTeX resume writer. Rewrite the resume in LaTeX format to better align with the JD. Keep all real experience, just rephrase and reorder to match the JD requirements."
        ),
        HumanMessage(
            content=f"Original Resume:\n{state['resume']}\n\nImprovements needed:\n{state['resolution']}"
        ),
    ]
    result = llm.invoke(messages)
    state["final_response"] = str(result.content).strip()
    return state
