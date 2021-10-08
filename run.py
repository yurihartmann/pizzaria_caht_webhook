import uvicorn

from main import app

uvicorn.run(app, port=8081)
