from agent import graph
from langchain_core.messages import HumanMessage

print("=" * 60)
print(" HR Attendance & Performance Bot ")
print("=" * 60)
print("Type 'exit' to quit.\n")

conversation = []

while True:

    question = input("You : ")

    if question.lower() == "exit":
        print("\nGoodbye!")
        break

    conversation.append(HumanMessage(content=question))

    result = graph.invoke({"messages": conversation})

    conversation = result["messages"]

    print("\nBot :", conversation[-1].content)
    print()
