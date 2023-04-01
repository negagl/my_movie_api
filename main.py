from fastapi import FastAPI

app = FastAPI()
app.title = 'My Movie API'
app.version = '0.0.1'


@app.get('/', tags=['home'])
def message():
    return 'hello world'


if __name__ == '__main__':
    message()
