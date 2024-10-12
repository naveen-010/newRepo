from openai import OpenAI
client = OpenAI()
p = input('you:')
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Extract event details like title, date, time, duration, locaiton, category from the user input and return them in a dictionary with their values entered by user.Time should be in 24 hr format, duration in minutes,date in DD-MM-YYYY format category like personal, work etc.Values that are not provided by user, fill them as 'None'.If user talk about anything else than adding event, tell them you are not there for it."},
        {
            "role": "user",
            "content": p, 
        }
    ]
)

out = completion.choices[0].message.content
print(out)
