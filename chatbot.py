from openai import OpenAI
from flask import Flask, request, render_template

client = OpenAI(
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = "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"
)
completion = client.chat.completions.create(
    model="nvidia/llama-3.1-nemotron-70b-instruct",
    messages=[{"role":"user","content":'for the following prompt, only write python code: '}],
    temperature=0.5,
    top_p=1,
    max_tokens=1024,
    stream=False
)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/process', methods=['POST'])
def process():
    #get the data from JS
    data = request.json
    text = data.get('text', '')

    #create an AI response using nvidia API
    condition = 'for the following prompt, write only python code. in the last line write # Relevant Variables and their Values: then write all relevant variables'
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role":"user","content":str(condition)+ text}],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=False
    )

    response = str(completion.choices[0].message)
    code = []

    #iterate through the list and capture executable lines of code in list 'code'
    for line in response.split("\\n"):
        #print(line) 
        try:
            exec(line)
            code += [line]
        except:
            #print("err " + line)
            pass

    #iterate through code statements and return results when correct statement is seen
    for i in range(len(code)):
        if code[i] == '# Relevant Variables and their Values:':
            return code[i:]
    return 'no significant values computed'

if __name__ == '__main__':
    app.run(debug=True)



