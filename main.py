from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models.models import questions, responses  # Import your model classes
from db import engine  # Import your database engine
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import logging
from fastapi.responses import JSONResponse


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create an instance of the FastAPI application
app = FastAPI()

# Set up CORS (Cross-Origin Resource Sharing) to allow requests from specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500", 
        "http://localhost:3000",
        "http://localhost:8000",
        "http://172.29.5.233:3000",
        "http://192.168.168.203:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Dependency to get a database session
def get_session():
    with Session(engine) as session:
        yield session

# Define a Pydantic model for contact submissions
class Contact(BaseModel):
    name: str
    email: str
    message: str

# POST endpoint to handle contact submissions
@app.post("/contact")
async def contact(contact: Contact, session: Session = Depends(get_session)):
    logger.info(f"Received contact from {contact.name} ({contact.email})")
    return {"message": "Your message has been received!"}

# Root endpoint for the API
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Formula 1 API! 🚗💨 Ask me anything about the 2023 season."
    }

# Generic function to create an item in the database
def create_generic(model):
    async def create(item: model, session: Session = Depends(get_session)):
        try:
            session.add(item)
            session.commit()
            session.refresh(item)
            logger.info(f"Created new {model.__name__}: {item}")
            return item
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating {model.__name__}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating {model.__name__}")
    return create

# Generic function to read an item from the database
def read_generic(model):
    async def read(item_id: int, session: Session = Depends(get_session)):
        item = session.get(model, item_id)
        if not item:
            logger.warning(f"{model.__name__} with id {item_id} not found")
            raise HTTPException(status_code=404, detail=f"{model.__name__} with id {item_id} not found")
        logger.info(f"Retrieved {model.__name__}: {item}")
        return item
    return read

# Generic function to update an item in the database
def update_generic(model):
    async def update(item_id: int, item: model, session: Session = Depends(get_session)):
        db_item = session.get(model, item_id)
        if db_item:
            item_data = item.dict(exclude_unset=True)
            for key, value in item_data.items():
                setattr(db_item, key, value)
            try:
                session.add(db_item)
                session.commit()
                session.refresh(db_item)
                logger.info(f"Updated {model.__name__}: {db_item}")
                return db_item
            except Exception as e:
                session.rollback()
                logger.error(f"Error updating {model.__name__}: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error updating {model.__name__}")
        logger.warning(f"{model.__name__} with id {item_id} not found for update")
        raise HTTPException(status_code=404, detail=f"{model.__name__} with id {item_id} not found")
    return update

# Generic function to delete an item from the database
def delete_generic(model):
    async def delete(item_id: int, session: Session = Depends(get_session)):
        item = session.get(model, item_id)
        if item:
            try:
                session.delete(item)
                session.commit()
                logger.info(f"Deleted {model.__name__} with id {item_id}")
                return {"ok": True}
            except Exception as e:
                session.rollback()
                logger.error(f"Error deleting {model.__name__}: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error deleting {model.__name__}")
        logger.warning(f"{model.__name__} with id {item_id} not found for deletion")
        raise HTTPException(status_code=404, detail=f"{model.__name__} with id {item_id} not found")
    return delete

# CRUD endpoints for Questions
@app.post("/questions/", response_model=questions)
async def create_question(item: questions, session: Session = Depends(get_session)):
    new_question = questions(question=item.question, created_at=datetime.now(timezone.utc))
    return await create_generic(questions)(new_question, session)

@app.get("/questions/{item_id}", response_model=questions)
async def read_question(item_id: int, session: Session = Depends(get_session)):
    return await read_generic(questions)(item_id, session)

@app.put("/questions/{item_id}", response_model=questions)
async def update_question(item_id: int, item: questions, session: Session = Depends(get_session)):
    return await update_generic(questions)(item_id, item, session)

@app.delete("/questions/{item_id}")
async def delete_question(item_id: int, session: Session = Depends(get_session)):
    return await delete_generic(questions)(item_id, session)

# CRUD endpoints for Responses
@app.post("/responses/", response_model=responses)
async def create_response(item: responses, session: Session = Depends(get_session)):
    new_response = responses(response_message=item.response_message, question_id=item.question_id, created_at=datetime.now(timezone.utc))
    return await create_generic(responses)(new_response, session)

@app.get("/responses/{item_id}", response_model=responses)
async def read_response(item_id: int, session: Session = Depends(get_session)):
    return await read_generic(responses)(item_id, session)

@app.put("/responses/{item_id}", response_model=responses)
async def update_response(item_id: int, item: responses, session: Session = Depends(get_session)):
    return await update_generic(responses)(item_id, item, session)

@app.delete("/responses/{item_id}")
async def delete_response(item_id: int, session: Session = Depends(get_session)):
    return await delete_generic(responses)(item_id, session)


# Endpoint to ask a question and retrieve a response
@app.get("/ask/{user_question}")
async def ask_question(user_question: str):
    logger.info(f"Received question: {user_question}")
    with Session(engine) as session:
        try:
            query = select(questions).where(questions.question.ilike(f"%{user_question}%"))
            result = session.exec(query).first()
            logger.info(f"Query result: {result}")

            if result:
                response_query = select(responses).where(responses.question_id == result.id)
                response = session.exec(response_query).first()
                logger.info(f"Response: {response}")
                return {
                    "question": result.question,
                    "response": response.response_message if response else "No response available.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            else:
                logger.info("No matching question found")
                return {"message": "I'm sorry, but I don't have information on that topic. Please try another question!"}
        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            raise HTTPException(status_code=500, detail="An error occurred while processing your question")

# Run the application
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the FastAPI application")
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Run on localhost at port 8000