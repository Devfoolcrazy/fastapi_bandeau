# CORE
from typing import Dict

# FASTAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# OWN UTILS
from files_utils.tools import load_rules_from_yaml
from ceh_utils.tools import apply_rules, format_matched_message, select_highest_priority_rule, get_meteo_for_location

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
    rules = load_rules_from_yaml("./rules_data/rules.yaml")
    matched_messages = apply_rules(ceh_data, rules)
    selected_message = select_highest_priority_rule(matched_messages)
    formatted_message = format_matched_message(selected_message)

    return formatted_message

@app.get("/health")
async def health_check():
    return {"status": "ok"}
