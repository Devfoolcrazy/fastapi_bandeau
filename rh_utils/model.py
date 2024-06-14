from pydantic import BaseModel

class Survey(BaseModel):
    question_id: int = None
    survey_name: str = None
    user_answer: str = None
    client_secret: str = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                "question_id": 1,
                "survey_name": "set_questions_reponses.csv",
                "user_answer": "la première donne de la thune, la seconde des moyens",
                "client_secret": "123456789"
                 }
            ]
        }
    }