from frontend.interface import UserInterface
from workflows.insurance_graph import InsuranceWorkflow
import asyncio

if __name__ == "__main__":
    router = InsuranceWorkflow()
    ui = UserInterface(router)
    asyncio.run(ui.run())