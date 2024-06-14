# CORE
from typing import Dict
import logging

# FASTAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# OWN UTILS
from rh_utils.tools import ask_question, get_question_by_id, evaluate_user_answer, check_if_authorized
from files_utils.tools import load_rules_from_yaml, load_csv
from ceh_utils.tools import apply_rules, format_matched_message, select_highest_priority_rule, get_meteo_for_location
from files_utils.tools import get_file_list

# MODELS
from rh_utils.model import Survey

app = FastAPI()

# CORS
origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "http://localhost:9000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:4173",
    "http://127.0.0.1:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)

# TODO mettre le load du yaml dans le context
@app.post("/ceh")
async def get_ceh_info(ceh_data: Dict):
    try:
        rules = load_rules_from_yaml("./rules_data/rules.yaml")
    except Exception as e:
        logging.error(e)
    
    try:
        matched_messages = apply_rules(ceh_data, rules)
    except Exception as e:
        logging.error(e)

    selected_message = select_highest_priority_rule(matched_messages)
    formatted_message = format_matched_message(selected_message)

    return formatted_message

@app.get("/health")
async def health_check():
    return {"status": "ok"}



@app.get("/rh/get_surveys")
async def get_rh_questionnaire():
    files = get_file_list('./data/rh_data')
    return {"surveys": files}


@app.post("/rh/get_question")
def rh_get_question(survey: Survey):
    try:
        survey = load_csv('./data/rh_data/' + survey.survey_name)
        question, question_id = ask_question(survey)

        return {"question": question, "id": int(question_id)}
    except Exception as e:
        logging.error(e)
        return {"error": str(e)}
    

@app.post("/rh/get_evaluation")
def rh_get_evaluation(survey: Survey):
    try:
        survey_data = load_csv('./data/rh_data/' + survey.survey_name)
        question, verified_answer = get_question_by_id(survey_data, int(survey.question_id))
        is_user_authorized = check_if_authorized(survey.client_secret)
        
        if not is_user_authorized:
            return {"error": "Unauthorized"}
        
        evaluation = evaluate_user_answer(question, verified_answer, survey.user_answer)

        return {"evaluation": evaluation}
    except Exception as e:
        logging.error(e)
        return {"error": str(e)}

