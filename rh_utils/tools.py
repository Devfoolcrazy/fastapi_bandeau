import os
from openai import OpenAI


def check_if_authorized(client_secret):
    actual_client_secret = os.environ.get("CLIENT_SECRET")
    if actual_client_secret == client_secret:
        return True
    else:
        return False
    
def ask_question(dataframe):
    # Choisis une ligne au hasard pour la question
    question_sample = dataframe.sample()
    question = question_sample['question'].iloc[0]
    verified_answer = question_sample['verified_answer'].iloc[0]
    id_answer = question_sample['id'].iloc[0]
    
    # Poser la question à l'utilisateur
    print(id_answer)
    
    return question, id_answer


def get_question_by_id(dataframe, id_answer):
    question_sample = dataframe[dataframe['id'] == id_answer]

    question = question_sample['question'].iloc[0]
    verified_answer = question_sample['verified_answer'].iloc[0]
    id_answer = question_sample['id'].iloc[0]
    
    return question, verified_answer

def evaluate_user_answer(question, verified_answer, user_response):
    # Envoi à l'API OpenAI pour évaluation
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    completion = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": """Tu es un formateur E-learning motivé et empathique. Tu as posé une question à un apprenant. Tu as la question, la réponse attendue et la réponse de l'utilisateur. Tu dois juger de la qualité de la réponse de l'apprenant. Si la réponse est correcte tu dois le faire savoir à ton apprenant, si elle est incompléte tu dois la compléter et féliciter l'apprenant sur ce qu'il a compris et retenu et si elle est fausse tu dois faire preuve de pédagogie et donner la réponse correcte en restant le plus positif possible.
        A la fin de ta réponse je veux une estimation en pourcentage de la validité de la réponse de ton apprenant.
        IMPORTANT:
        - Tu parles en Français.
        - Vouvoie ton apprenant.
        - Ne sois pas condescendant.
        - N'explique pas ta démarche pédagogique dans ta réponse.
        - Ta réponse devra prendre la forme d'un json avec un clef response et une clef score (le score est un integer entre 0 et 100)
         """},
        {"role": "user", "content": f"Question: {question}\nRéponse vérifiée: {verified_answer}\nRéponse utilisateur: {user_response}\nÉvaluer la réponse."}
    ], 
    response_format={"type": "json_object"}

    )
    return completion.choices[0].message.content