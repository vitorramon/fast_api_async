from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_api_async.schemas import Message

app = FastAPI(title='Minha API')


@app.get('/',
         status_code=HTTPStatus.OK,
         response_model=Message
         )
def read_root():
    return {'message': 'Olá mundo!'}


@app.get('/pagina-test',
         status_code=HTTPStatus.OK,
         response_class=HTMLResponse
         )
def read_hello():
    return """
    <html>
        <head>
            <title>FastAPI Async Example</title>
        </head>
        <body>
            <h1>Olá mundo!</h1>
        </body>
    </html>
    """
