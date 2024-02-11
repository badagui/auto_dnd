# to start api run python main_api.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.main_api:app", host="127.0.0.1", port=8000)
