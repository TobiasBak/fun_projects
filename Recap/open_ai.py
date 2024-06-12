


def generate_text(prompt, api_key):
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the content of the assistant's reply
    reply = response.choices[0].message['content']

    return reply