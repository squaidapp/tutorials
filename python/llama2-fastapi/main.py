import copy
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from llama_cpp import Llama

#Create Question Model
class Question(BaseModel):
    author: str | None = None
    question: str 

#Loading model
print('Loading model...')
llm = Llama(model_path="/home/blabla/llama-2-13b-chat.ggmlv3.q4_0.bin")
print('Model loaded, lets rock!')

#Create App
app = FastAPI()

#Define function for Llama2 Streaming
def answer_question(question: Question) -> str:
    stream = llm( f"Question: {question.question} Answer:",
                max_tokens=250,
                stop=["/n","Question:", "Q:"],
                stream=True
                )
    print('Answer starts...')

    for out in stream:
        completionFragment = copy.deepcopy(out)
        yield completionFragment['choices'][0]['text']

#Create Method
@app.post('/streaming/')
async def main(question: Question):
    return StreamingResponse(answer_question(question), media_type='text/event-stream')