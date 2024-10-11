from openai import OpenAI
client = OpenAI()
a = 1
while a != 'q':
    a = input('You: ')
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Abuse brutally."},
            {
                "role": "user",
                "content": a,
            }
        ]
    )

    print(completion.choices[0].message.content)
