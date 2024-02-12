# to run fastapi local server: python main_api.py
# to run in production with multiple workers (linux): gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main_api:app
import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.main_api:app", host="127.0.0.1", port=8000)
