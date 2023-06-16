
def process_gpt(inputs):
    input1 = inputs[0]
    input2 = inputs[1]
    input3 = inputs[2]

    conversations = []

    conversations.append({
        'role': 'system',
        'content': f'Please read {input1} and create me 5 short SEO keywords around {input2} located in {input3}'
    })
    result = chatgpt_conversation(conversations)
    # Open a file to write to
    # with open('output.txt', 'w') as f:
    #     # Write the response from the dashboard.html file to the file
    #     f.write(response.text)

    # while True:
    #     prompt = input('User: ')
    #     result.append({'role': 'user', 'content': prompt})
    #     result = chatgpt_conversation(result)
    #     print()
    #     print('{0}: {1}\n'.format(result[-1]['role'].strip(), result[-1]['content'].strip()))
    #     print(response.text)

    return '{0}: {1}\n'.format(result[-1]['role'].strip(), result[-1]['content'].strip())
