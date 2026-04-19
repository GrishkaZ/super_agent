import os
from dotenv import load_dotenv
import requests
import json

load_dotenv('.env')

qwen_token = os.getenv('QWEN_TOKEN')

def req_qwen(prompt, reasoning=False):
    url = "https://qwen.aikit.club/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {qwen_token}",
        "Content-Type": "application/json"
    }

    stream = False
    data = {
        "model": "qwen3.5-plus",
        "messages": [
            {"role": "system", "content": "Answer as if you were an aristocrat from the 19th century."},
            {"role": "user", "content": prompt}
        ],
        "enable_thinking": reasoning,
        "stream": stream
    }

    response = requests.post(url, headers=headers, json=data, stream=stream)
    print(response)
    result = json.loads(response.text)['choices'][0]['message']['content']

    result = result.split('<details>')[0]
    print(result)
    return result


if __name__ == '__main__':
    req_qwen('Hello, how are you?')
