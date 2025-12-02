from agents.router_agent import RouterAgent
from workflows.insurance_graph import InsuranceWorkflow
from workflows.orchestrator_workflow import workflow

class UserInterface:
    def __init__(self, app: InsuranceWorkflow):
        self.app = app

    async def run(self):
        while True:
            query = input("Bạn: ")
            if query.lower() in ["quit", "exit"]:
                break
            result = await workflow.run(query)
            response = result["messages"][-1].content
            print("Bot:", response)