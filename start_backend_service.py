from backend import app
import uvicorn
import config

uvicorn.run(app, host=config.BACKEND_HOST, port=config.BACKEND_PORT)
