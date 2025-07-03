# 📄 test_graph_message.py
# Test du LangGraph avec agent_message
import os
os.environ["LANGCHAIN_API_KEY"] = ""
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_ENDPOINT"] = ""
os.environ["LANGCHAIN_PROJECT"] = ""

from model.graph.message_graph import graph

if __name__ == "__main__":
    print("=== Test LangGraph SeductAI : agent_message ===")
    question = input("🗨️  Ta question à l'IA :\n> ")

    result = graph.invoke({"question": question})
    
    print("\n🧠 Réponse générée :\n")
    print(result["response"])
