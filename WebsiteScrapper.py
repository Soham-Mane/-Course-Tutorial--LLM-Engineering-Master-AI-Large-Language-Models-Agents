import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import ollama

MODEL = "llama3.2"

class Website:
    """
    A utility class to represent a Website that was scrapped.
    """

    url: str
    title: str
    text: str
    
    def __init__(self,url):
        """
        Create this website object from given url using the BeautifulSoup library
        """
        self.url= url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else 'No title found'
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

ed = Website("https://edwarddonner.com")
print(ed.title)
print(ed.text)   

system_prompt="You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

def user_prompt_for(website):
    user_prompt=f"You are looking for a webiste titled {website.title}"
    user_prompt+="The contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt+=website.text
    return user_prompt

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]
def summarize(url):
    website=Website(url)
    messages=messages_for(website)
    response=ollama.chat(model=MODEL, messages=messages)
    return response['message']['content']
summarize("https://timesofindia.indiatimes.com/")  

def display_summary(url):
    summary=summarize(url)
    display(Markdown(summary))
display_summary("https://www.tle-eliminators.com/cp-sheet")   
