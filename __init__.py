import logging
import openai
import os
import json
import azure.functions as func

openai.api_key = os.getenv('OPENAI_API_KEY')

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        req_body = req.get_json()
        user_input = req_body.get('user_input')

        if user_input:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_input,
                max_tokens=150
            )
            return func.HttpResponse(
                json.dumps({"response": response.choices[0].text.strip()}),
                mimetype="application/json",
                status_code=200
            )
        else:
            return func.HttpResponse(
                "Please pass a user_input in the request body",
                status_code=400
            )
    except Exception as e:
        logging.error(f'Error: {str(e)}')
        return func.HttpResponse(
            "Error processing request",
            status_code=500
        )