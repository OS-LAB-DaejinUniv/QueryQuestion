from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google import genai
from google.genai import types
from dotenv import load_dotenv
import markdown

load_dotenv()

client = genai.Client()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/llmquestion/{question}", response_class=HTMLResponse)
async def get_answer(request:Request,
                     question:str):
    """
    - Query String으로 질문을 하면 HTML을 응답하여 해당 질문에 대한 답변을 제공합니다.
    - Ex) http://localhost:8000/오늘뭐먹지?
    """
    try: 
        # 모델에 질문 전달
        response = client.models.generate_content(
            contents=question,
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0) # Disable Thinking
            ),
        )
        answer_html = markdown.markdown(response.text, extensions=['fenced_code', 'nl2br'])
        answer_raw = response.text
    except Exception as e:
        print(f"제미나이가 답변을 생성하는데 오류가 생겼습니다.{e}")
        answer = "미안함다. 질문에 대한 답변하다가 오류 생겨버렸슴다."
    
    return templates.TemplateResponse(
        "answer.html",
        {"request":request, 
         "question": question,
         "answer" : answer_html
        }
    )
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)