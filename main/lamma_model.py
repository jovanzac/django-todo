import os
from groq import Groq


class LammaLLM :
    def __init__(self) :
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    def prompt_the_llm(self, prompt, context="") :
        completion = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": f"""Give me specific suggestions on how to perform the following task. 
                        If no specific suggestion can be offered, then list the besefits of doing the task
                        to motivate the user. Use the following as context: {context}"""
                },
                {
                    "role": "user",
                    "content": f"{prompt}"
                },
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        content = completion.choices[0].message.content
        return content