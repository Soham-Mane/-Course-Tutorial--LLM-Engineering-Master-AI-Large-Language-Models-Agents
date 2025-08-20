import ollama
import os
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai
import gradio as gr # oh yeah!


load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set")


google.generativeai.configure()


def shout(text):
    print(f"Shout has been called with input  {text}")
    return text.upper()

shout("hello")


def llama_response(user_input: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input},
    ]
    response = ollama.chat(model="llama3.2", messages=messages)
    return response['message']['content']

def gemini_response(user_input: str) -> str:
    gemini= google.generativeai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction="You are a helpful assistant."
    )
    response=gemini.generate_content(user_input)
    return response.text

def chat_with_model(user_input: str, model_choice: str) -> str:
    if model_choice== "llama":
        return llama_response(user_input)
    elif model_choice== "gemini":
        return gemini_response(user_input)
    
demo = gr.Interface(
    fn=chat_with_model,
    inputs=[
        gr.Textbox(label="Enter your message."),
        gr.Dropdown(choices=["llama", "gemini"], label="Choose Model", value="llama")
    ],
    outputs=gr.Textbox(label="Model Response"),
    title="Multi-Model Chat",
    description="Chat with either Llama or Gemini by selecting from the dropdown."
)    

demo.launch(inbrowser=True)