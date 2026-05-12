import os
import json
from pydantic import BaseModel
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_google_genai  import ChatGoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv()

# read playbook.json file
with open("playbooks.json", "r", encoding="utf-8") as f:
    PLAYBOOKS = json.load(f)

# initialize resoonse format
class ResponseFormat(BaseModel):
    threat_type: str
    display_name: str
    description: str
    severity: str
    response_steps: list[str]
    recommended_tools: list[str]

# Tools
@tool("get_playbook", return_direct=True, description="Get the playbook for a specific threat type. Input should be the threat type.")
def get_playbook(threat_type: str) -> str:
    """
    Get the playbook for a specific threat type. as a json string.
    """

    playbooks = PLAYBOOKS.get("playbooks", [])

    for playbook in playbooks:

        if playbook["threat_type"].lower() == threat_type.lower():

            return json.dumps(playbook, indent=2)

    return f"No playbook found for threat type: {threat_type}"

# Initialize the model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY")
)

# system prompt for the agent
SYSTEM_PROMPT = """
You are an AI SOC Analyst Agent.

Your responsibilities:
- Analyze security logs
- Identify the cyber threat type
- Retrieve the appropriate SOC playbook
- Generate a professional incident response report

Available threat types:
- brute_force
- phishing
- credential_stuffing
- ransomware
- malware
- suspicious_powershell
- data_exfiltration
- insider_threat
- privilege_escalation
- lateral_movement
- command_and_control
- web_shell
- sql_injection
- ddos
- suspicious_login
- impossible_travel
- token_theft
- api_abuse
- dns_tunneling
- crypto_mining

Rules:
1. First analyze the logs carefully
2. Determine the threat type
3. Use the get_playbook tool
4. Generate a professional followed by reponse format that i provided you with

The report should follow response format
"""
# initialize the agent with the tools
agent =  create_agent(
    model=model,
    tools=[get_playbook],
    system_prompt=SYSTEM_PROMPT,
    response_format=ResponseFormat
)

structured_model = model.with_structured_output(ResponseFormat)
def analyze_logs(logs: str):

    analysis = agent.invoke({
        "messages": [
            ("user", f"Analyze these logs:\n{logs}")
        ]
    })

    final_response = structured_model.invoke(
        f"""
        Convert the following SOC analysis into the exact ResponseFormat schema.

        Analysis:
        {analysis["messages"][-1].content}
        """
    )

    return final_response