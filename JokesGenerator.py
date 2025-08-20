import os
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display, update_display
import google.generativeai
import requests

print("Using gemini and deepseek api key as chatgpt and claude quota exceeded")

load_dotenv(override=True)
google_api_key=os.getenv('GOOGLE_API_KEY')
deepseek_api_key=os.getenv('DEEPSEEK_API_KEY')
if(google_api_key):
    print(f"Google api key exists and begins {google_api_key[:8]}")
else:
    print("Google API key not set")

if(deepseek_api_key):
    print(f"Deep seek api exists and begins {deepseek_api_key[:8]}")
else:
    print("Deep seek key not set")    

google.generativeai.configure()    

system_message="You are an assistant that is great at telling jokes"
user_prompt="Tell a light-hearted joke for an audience of LLM Engineer"

prompts =[
    {"role" : "system", "content": system_message},
    {"role": "user", "content": user_prompt}
]

gemini=google.generativeai.GenerativeModel(
    model_name='gemini-2.0-flash',
    system_instruction=system_message
)

response = gemini.generate_content(user_prompt)
print(response.text)

# As an alternative way to use Gemini that bypasses Google's python API library,
# Google released endpoints that means you can use Gemini via the client libraries for OpenAI!
# We're also trying Gemini's latest reasoning/thinking model

gemini_via_openai_client = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = gemini_via_openai_client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=prompts
)

print(response.choices[0].message.content)   #successful using openAI and passing gemini's api key.

# Using DeepSeek Chat

# Using DeepSeek Chat

deepseek_via_openai_client = OpenAI(
    api_key=deepseek_api_key, 
    base_url="https://api.deepseek.com"
)

response = deepseek_via_openai_client.chat.completions.create(
    model="deepseek-chat",
    messages=prompts,
)

print(response.choices[0].message.content)

# Using DeepSeek Chat with a harder question! And streaming results

stream = deepseek_via_openai_client.chat.completions.create(
    model="deepseek-chat",
    messages=challenge,
    stream=True
)

reply = ""
display_handle = display(Markdown(""), display_id=True)
for chunk in stream:
    reply += chunk.choices[0].delta.content or ''
    reply = reply.replace("```","").replace("markdown","")
    update_display(Markdown(reply), display_id=display_handle.display_id)

print("Number of words:", len(reply.split(" ")))
