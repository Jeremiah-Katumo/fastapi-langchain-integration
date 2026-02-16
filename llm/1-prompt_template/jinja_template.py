from langchain_core.prompts import PromptTemplate

jinja_template = """
You are analyzing customer support tickets to determine the sentiment of the customer's message. Here are the last 3  tickets:
{% for ticket in tickets %}
Ticket #{{ loop.index }}:{{ ticket }} 
Status: {{ ticket.status }}
{% endfor %} 

Based on the above tickets, determine the overall sentiment of this new ticket: '{{ new_ticket }}'
"""

prompt = PromptTemplate.from_template(jinja_template, template_format="jinja2")

ticket_history = [
    {"text": "My login does not work", "status": "resolved"},
    {"text": "Password reset needed", "status": "in progress"},
    {"text": "App is crashing", "status": "opened"}
]

result = prompt.format(tickets=ticket_history, new_ticket="I can't access my account")
print(result)