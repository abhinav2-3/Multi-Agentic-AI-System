from langgraph.graph import StateGraph, END

from src.agents.classifier import SupportState

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
        "query": "I was charged twice for my subscription this month",
        "category": "",
        "resolution": "",
        "final_response": "",
    }
)

print("Category:", result["category"])
print("Resolution:", result["resolution"])
print("Final Response:", result["final_response"])
