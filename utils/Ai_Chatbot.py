# Preserved original AI chatbot code as a utility module
API_KEY = "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"
MODEL = "mistralai/mixtral-8x7b-instruct"

def get_ai_response(question):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": question}]
    }
    try:
        response = requests.post(url, headers=headers, json=body)
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error: {result}"
    except Exception as e:
        return f"Error: {str(e)}"