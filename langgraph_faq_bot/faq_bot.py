from dataclasses import dataclass
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda

# ✅ FAQ data
faq_data = {
    "What is Python?": "Python is a popular high-level programming language known for its simplicity and readability.",
    "What is LangGraph?": "LangGraph is a framework for building stateful, multi-step applications using language models.",
    "How do I install LangGraph?": "You can install LangGraph using the command: pip install langgraph.",
    "What is an LLM?": "LLM stands for Large Language Model.",
    "Can I use LangGraph with OpenAI?": "Yes, LangGraph works well with OpenAI.",
}

# ✅ Define schema using dataclass
@dataclass
class FAQState:
    question: str
    answer: str = ""

# ✅ Function to find best answer
def find_best_answer(state: FAQState):
    user_question = state.question.lower()
    for q, a in faq_data.items():
        if user_question in q.lower() or q.lower() in user_question:
            return FAQState(question=state.question, answer=a)
    return FAQState(question=state.question, answer="Sorry, I couldn't find an answer to that question.")

# ✅ Set up LangGraph node
faq_node = RunnableLambda(find_best_answer)

# ✅ Build LangGraph flow
graph = StateGraph(state_schema=FAQState)
graph.add_node("faq", faq_node)
graph.set_entry_point("faq")
graph.set_finish_point("faq")
faq_app = graph.compile()

# ✅ Chat loop
while True:
    user_input = input("\nAsk a question (or type 'exit' to quit): ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    result = faq_app.invoke({"question": user_input})
    print("Answer:", result["answer"])
