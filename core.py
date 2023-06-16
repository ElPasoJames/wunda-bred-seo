import openai
import os
import requests

API_KEY = 'XXXXXXX'
openai.api_key = API_KEY
model_id = 'gpt-3.5-turbo-0301'

def chatgpt_conversation(conversation_log):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation_log
    )

    conversation_log.append({
        'role': response.choices[0].message.role, 
        'content': response.choices[0].message.content.strip()
    })
    return conversation_log

# Get the HTML code from the dashboard.html file
response = requests.get('/templates/dashboard.html')

conversations = []
# system, user, assistant
conversations['input1'] = input1
conversations['input2'] = input2
conversations['input3'] = input3
conversations.append({'role': 'system', 'content': 'Please read ['input1'] and create me 5 short SEO keywords around ['input2'] located in ['input3']})
conversations = chatgpt_conversation(conversations)
print('{0}: {1}\n'.format(conversations[-1]['role'].strip(), conversations[-1]['content'].strip()))

while True:
    prompt = input('User: ')
    conversations.append({'role': 'user', 'content': prompt})
    conversations = chatgpt_conversation(conversations)
    print()
    print('{0}: {1}\n'.format(conversations[-1]['role'].strip(), conversations[-1]['content'].strip()))
