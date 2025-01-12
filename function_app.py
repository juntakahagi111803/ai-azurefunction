import azure.functions as func
import logging
import openai

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger1")
def http_trigger1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_input = req.params.get('user_input')
    if not user_input:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            user_input = req_body.get('user_input')

    if user_input:
        return func.HttpResponse("Hello, . This HTTP triggered function executed successfully!!!!!!!!!!!!!!")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )