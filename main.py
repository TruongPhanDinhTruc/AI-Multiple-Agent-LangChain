from frontend.interface import UserInterface
from workflows.insurance_graph import InsuranceWorkflow

if __name__ == "__main__":
    router = InsuranceWorkflow()
    ui = UserInterface(router)
    ui.run()