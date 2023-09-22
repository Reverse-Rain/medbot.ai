import openai

# Set up your OpenAI API credentials
openai.api_key = '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'

# Function to check if GPT-3 response is correct

# Function to ask GPT-3 using Completion API
def ask_gpt(question):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=question,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

