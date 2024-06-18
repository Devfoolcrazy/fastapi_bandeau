from pydantic import BaseModel

class UserAnswer(BaseModel):
    user_answer: str
    client_secret: str = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                "user_answer": "la voiture de démarre pas",
                "client_secret": "123456789"
                 }
            ]
        }
    }