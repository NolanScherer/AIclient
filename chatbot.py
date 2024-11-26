from openai import OpenAI
from flask import Flask, request, render_template

client = OpenAI(
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = "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"
)
completion = client.chat.completions.create(
    model="nvidia/llama-3.1-nemotron-70b-instruct",
    messages=[{"role":"user","content":'for the following prompt, only write python code: write a list of 10 random integers'}],
    temperature=0.5,
    top_p=1,
    max_tokens=1024,
    stream=True
)

ans = ''
for chunk in completion:
    if chunk.choices[0].delta.content is not None:
        try:
            print(chunk.choices[0].delta.content)
            exec(chunk.choices[0].delta.content)
            ans += chunk.choices[0].delta.content
        except:
            pass

code = ans.split('\n')
print(code)
res = ''
i = 0
functions = []
while i < len(code):
    if code[i].startswith('def'):
        func = code[i]
        i+=1
        while code[i].startswith('\t'):
                func+=code[i] + '\n'
                i+=1
        functions += func

    if code[i].startswith('print'):
        thing = code[i][6:-1]
        if thing in globals():
            res += globals()[thing] + '\n'


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/process', methods=['POST'])
def process():
    #get the data from JS
    data = request.json
    text = data.get('text', '')


    return res

if __name__ == '__main__':
    app.run(debug=True)

# while True:
#     request = input('ask ai something, or enter \'done\' to quit -> ')
#     if request == 'done':
#         break

