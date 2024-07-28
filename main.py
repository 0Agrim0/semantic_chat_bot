from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from router_chain import function_router  # Assuming this is where your function_router is defined

app = FastAPI()

class QuestionPayload(BaseModel):
    question: str

class PhoneNumber(BaseModel):
    phone_number: str

@app.post("/")
async def root(request: Request, question_payload: QuestionPayload):
    try:
        # Accessing question from the request body
        print(question_payload)
        question = question_payload.question
        print(f"Received question: {question}")

        # Accessing phone number from headers
        phone_number_header = request.headers.get('phone')
        if not phone_number_header:
            raise HTTPException(status_code=400, detail="Phone number header not provided")

        # Call your function_router with phone number and question
        print(f"Received phone number header: {phone_number_header}")
        result = function_router(phone_number_header).router(question)
        return {"result": result}

    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
