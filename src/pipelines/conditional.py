import operator

from langgraph.graph import START, StateGraph, END
from typing import Annotated, TypedDict
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, SecretStr

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=SecretStr(os.getenv("GROQ_API_KEY") or ""),
)


# class EvaluationSchema(BaseModel):
#     feedback: str = Field(description="Detailed feedback of the essay")
#     score: int = Field(description="Score out of 10", ge=0, le=10)


# structured_model = llm.with_structured_output(EvaluationSchema)


class EssayState(TypedDict):
    content: str
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: str
    individual_scores: Annotated[list[int], operator.add]
    avg_score: float


def evaluate_language(state: EssayState) -> dict:
    prompt = f"Evaluate the language quality of the following essay and provide a feedback and assign a score out of 10\n\n{state['essay']}"
    output = structured_model.invoke(prompt)
    assert isinstance(output, EvaluationSchema)
    return {"language_feedback": output.feedback, "individual_scores": [output.score]}


def evaluate_analysis(state: EssayState) -> dict:
    prompt = f"Evaluate the depth of analysis of the following essay and provide a feedback and assign a score out of 10\n\n{state['essay']}"
    output = structured_model.invoke(prompt)
    assert isinstance(output, EvaluationSchema)
    return {"analysis_feedback": output.feedback, "individual_scores": [output.score]}


def evaluate_thought(state: EssayState) -> dict:
    prompt = f"Evaluate the clarity of thought of the following essay and provide a feedback and assign a score out of 10\n\n{state['essay']}"
    output = structured_model.invoke(prompt)
    assert isinstance(output, EvaluationSchema)
    return {"clarity_feedback": output.feedback, "individual_scores": [output.score]}


def final_evaluation(state: EssayState) -> dict:
    prompt = f"Based on the follwoing feedbacks create a summarized feedback \n language feedback - {state['language_feedback']},\n depth analysis feedback - {state['analysis_feedback']} \n clarity feedback - {state['clarity_feedback']}"
    output = str(llm.invoke(prompt).content)

    avg_score = sum(state["individual_scores"]) / len(state["individual_scores"])

    return {"overall_feedback": output, "avg_score": avg_score}


graph = StateGraph(EssayState)

graph.add_node("evaluate_language", evaluate_language)
graph.add_node("evaluate_analysis", evaluate_analysis)
graph.add_node("evaluate_thought", evaluate_thought)
graph.add_node("final_evaluation", final_evaluation)

graph.add_edge(START, "evaluate_language")
graph.add_edge(START, "evaluate_analysis")
graph.add_edge(START, "evaluate_thought")

graph.add_edge("evaluate_language", "final_evaluation")
graph.add_edge("evaluate_analysis", "final_evaluation")
graph.add_edge("evaluate_thought", "final_evaluation")

graph.add_edge("final_evaluation", END)

workflow = graph.compile()

essay = """Pollution is one of the most serious environmental challenges we face today. It refers to the contamination of natural elements like air, water, and soil, and even includes excessive noise and light that disturb the balance of life. Pollution is primarily caused by human activities such as burning fossil fuels, cutting down forests, improper disposal of industrial and household waste, and the use of non-biodegradable materials like plastic.

Air pollution is caused by the release of harmful gases from vehicles, factories, and burning of garbage. It leads to breathing problems, asthma, and increases the risk of lung cancer. It also plays a major role in global warming and climate change. Water pollution occurs when industrial waste, plastic, and sewage are dumped into rivers and oceans. It harms marine life and makes water unsafe for human use. Soil pollution reduces the fertility of land due to chemicals and waste, affecting food production. Noise pollution from honking vehicles, construction work, and loudspeakers causes stress, hearing issues, and disturbs both humans and animals.

To fight pollution, we must act responsibly. Using public transport, recycling, conserving electricity, switching to renewable energy, and avoiding plastic are good starting points. Governments should also enforce strict environmental laws.

Children can play a major role in protecting the environment. They can plant trees, say no to plastic, conserve water and energy, and spread awareness through essays, drawings, and storytelling.

If each one of us takes small steps, we can together build a cleaner and greener future."""


initial_state: EssayState = {
    "essay": essay,
    "language_feedback": "",
    "analysis_feedback": "",
    "clarity_feedback": "",
    "overall_feedback": "",
    "individual_scores": [],
    "avg_score": 0.0,
}

result = workflow.invoke(initial_state)


print("Result \n", result)
