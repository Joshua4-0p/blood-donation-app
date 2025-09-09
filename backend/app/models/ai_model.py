from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from datetime import datetime
import json



# Initialize Groq model
llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="mixtral-8x7b-32768")

# Prompt template
prompt_template = """
Analyze this health questionnaire: {questionnaire}
Donation history: Last donation on {last_donation_date} (or None if no history).
Evaluate eligibility based on WHO/FDA rules:
- Age 18-65
- Weight >50kg (assume from questionnaire)
- No recent illness, travel to high-risk areas, tattoos (<6 months), pregnancy, etc.
- Minimum 56 days since last donation.
Output JSON: {{"eligible": bool, "reason": str}}
"""

eligibility_prompt = PromptTemplate(
    input_variables=["questionnaire", "last_donation_date"],
    template=prompt_template
    
)

# New style: RunnableSequence
eligibility_chain = eligibility_prompt | llm

def check_eligibility(questionnaire: dict, last_donation_date: datetime = None):
    last_date_str = last_donation_date.strftime("%Y-%m-%d") if last_donation_date else "None"
    response = eligibility_chain.invoke({
        "questionnaire": str(questionnaire),
        "last_donation_date": last_date_str
    })

    # Handle the model response safely
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {"eligible": False, "reason": f"Invalid response: {response.content}"}
