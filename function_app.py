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

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
@app.function_name(name="http_trigger1")
@app.route(route="http_trigger1")

#環境変数OPENAI_API_KEYからAPIキーを取得して設定します。
#openai.api_key = os.getenv('OPENAI_API_KEY')

#メイン関数定義 - この関数はHTTPリクエストが来たときに実行されます。
def http_trigger1(req: func.HttpRequest) -> func.HttpResponse:

    #リクエストのログ出力:HTTPトリガー関数がリクエストを処理したことをログに記録します。
    logging.info('Python HTTP trigger function processed a request.')
    
    user_input = req.params.get('user_input')
    #リクエスト処理の試み:
    #受け取ったリクエストボディをJSON形式で解析し、user_inputを取得します。
    #HTTPリクエストボディからユーザーの入力データ（user_input）を取得するためのものです。
    #
    #つまり、Azure Static Web Appsに登録した、htmlに記載のjavascriptで[user_input]を定義しているそのこと！
    #htmlのテキストボックスに入力してOKボタンをクリックすると！javascriptがその値を取得し[user_input]としてあつかう！
    #そのデータはHttpリクエストとなり、このAzureFunctionsのファイルに届いてくる！
    #そのリクエストBody部分に記載された、キー[user_input]部分に対応しているデータを取得しており(req_body.getで)、
    #それをこっちのPython側の変数[user_input]に格納した。ということ。
    try:
        #この行はHTTPリクエストボディをJSON形式で解析し、その結果を req_body という変数に代入します。
        req_body = req.get_json()
        #req.get_json() は、リクエストボディがJSONフォーマットの場合にそのデータをPythonの辞書型オブジェクトとして返します
        #req_body が辞書型オブジェクトであるため、 req_body.get('user_input') を使って 'user_input' というキーを検索し、その値を user_input に代入します。
        #get メソッドを使うことで、該当するキーが存在しない場合には None を返します。これにより、キーが存在しない場合でもプログラムがエラーで停止することを防いでいます。
        user_input = req_body.get('user_input')

        #入力の確認と応答生成:
            #user_inputが存在する場合、OpenAIのAPIを呼び出し、text-davinci-003エンジンを使って応答を生成します。生成された応答をJSON形式で返します。
            #user_inputが存在しない場合は、入力が足りないことを知らせるレスポンスを返します。

        #user_input が None でないかどうかを確認しています。存在する場合は次の処理に進みます。
        if user_input:
            #Completion.createの呼び出し:
                #openai.Completion.create メソッドを使用して、OpenAIのAPIにリクエストを送ります。
                #engine パラメータには、使用するGPTモデルの名前(text-davinci-003)を指定しています。
                #prompt パラメータには、ユーザーの入力 (user_input) を渡します。つまりAzure Static Web App に登録したhtmlのjavascrpit部分
                #max_tokens パラメータには、生成する応答の最大トークン数 (150トークン) を指定しています。
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_input,
                max_tokens=150
            )

            #HTTPレスポンスの生成:
                #OpenAI APIからの応答 response のテキスト部分を取得し、JSON形式に変換してHTTPレスポンスを生成します。
                #response.choices[0].text.strip() で、API応答の最初の候補のテキストを取り出し、前後の空白を取り除いています。
                #生成したレスポンスは、application/json のMIMEタイプを持つステータスコード200（成功）で返されます。
            return func.HttpResponse(
                json.dumps({"response": response.choices[0].text.strip()}),
                mimetype="application/json",
                status_code=200
            )
        else:
            #user_inputがなかった場合の処理
            #この部分のコードは、user_input が存在しない場合に実行されます。
            #user_input が存在しない場合、この else ブロックが実行されます。
            #エラーメッセージ「Please pass a user_input in the request body!」を含むHTTPレスポンスをステータスコード400（リクエストのエラー）で返します。
            return func.HttpResponse(
                "Please pass a user_input in the request body!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!But!!Azure Static Web AppsからAzure連携は成功!!!!!!!!!!!!!!!!!!!!!!!!",
                status_code=400
            )
        
    #エラーハンドリング:例外が発生した場合、エラーログを記録し、エラーメッセージを含むレスポンスを返します。    
    except Exception as e:
        logging.error(f'Error: {str(e)}')
        return func.HttpResponse(
            "Error processing request",
            status_code=500
        )