from openai import OpenAI

client = OpenAI(
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = "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"
)
while True:
    request = input('ask ai something, or enter \'done\' to quit -> ')
    if request == 'done':
        break

    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role":"user","content":'write nothing except excecutable python code for this request: ' + request},],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=True
    )

    ans = ''
    go = True
    for chunk in completion:
        if chunk.choices[0].delta.content not in (None, '```python'):

            if go:
                ans += chunk.choices[0].delta.content
    for line in ans.split('\n'):
            try:
                exec(line)
            except:
                pass
