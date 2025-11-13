from agents.router_agent import RouterAgent
from workflows.insurance_graph import InsuranceWorkflow

class UserInterface:
    def __init__(self, app: InsuranceWorkflow):
        self.app = app

    def run(self):
        while True:
            query = input("Bạn: ")
            if query.lower() in ["quit", "exit"]:
                break
            result = self.app.run(query)
            response = result["messages"][-1].content
            print("Bot:", response)