#このプログラムは、Azure Functionsを使用してHTTPリクエストを処理し、
#OpenAIのAPIを使って応答を生成する機能を持っています。
#
#
#    - `logging`: ロギングを管理するための標準ライブラリ。
#    - `openai`: OpenAIのAPIを利用するためのライブラリ。
#    - `os`: 環境変数を操作するための標準ライブラリ。
#    - `json`: JSONデータを操作するための標準ライブラリ。
#    - `azure.functions as func`: Azure FunctionsのHTTPトリガーを使うためのライブラリ。
#
import logging
import openai
import os
import json
import azure.functions as func

#環境変数OPENAI_API_KEYからAPIキーを取得して設定します。
openai.api_key = os.getenv('OPENAI_API_KEY')

#メイン関数定義 - この関数はHTTPリクエストが来たときに実行されます。
def main(req: func.HttpRequest) -> func.HttpResponse:

    #リクエストのログ出力:HTTPトリガー関数がリクエストを処理したことをログに記録します。
    logging.info('Python HTTP trigger function processed a request.')
    
    #リクエスト処理の試み:受け取ったリクエストボディをJSON形式で解析し、user_inputを取得します。
    try:
        req_body = req.get_json()
        user_input = req_body.get('user_input')

        #入力の確認と応答生成:
            #user_inputが存在する場合、OpenAIのAPIを呼び出し、text-davinci-003エンジンを使って応答を生成します。生成された応答をJSON形式で返します。
            #user_inputが存在しない場合は、入力が足りないことを知らせるレスポンスを返します。
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
                "Please pass a user_input in the request body!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!But!!Azure Static Web AppsからAzure Functionへの連携は成功！！！",
                status_code=400
            )
        
    #エラーハンドリング:例外が発生した場合、エラーログを記録し、エラーメッセージを含むレスポンスを返します。    
    except Exception as e:
        logging.error(f'Error: {str(e)}')
        return func.HttpResponse(
            "Error processing request",
            status_code=500
        )