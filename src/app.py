import os
import logging
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
# from github import Github

app = FastAPI()

# Load environment variables
logging.basicConfig(level=logging.DEBUG)

PRIVATE_KEY = os.getenv('GITHUB_PRIVATE_KEY')
WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET')
APP_ID = os.getenv('GITHUB_APP_IDENTIFIER')
# GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
# REPO_NAME = os.getenv('REPO_NAME')

# # Initialize GitHub client
# github = Github(GITHUB_TOKEN)
# repo = github.get_repo(REPO_NAME)

@app.get("/")
async def root():
    return {"message": "Hello, this is CodeSA App!"}

@app.post("/event_handler")
async def webhook(request: Request, x_github_event: str = Header(None)):
    payload = await request.json()

    if x_github_event == 'push':
        handle_push_event(payload)
    # Add more event handlers as needed

    return JSONResponse(content={"status": "success"})

def handle_push_event(payload):
    # Example: Print commit messages
    for commit in payload['commits']:
        print(f"Commit message: {commit['message']}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=3000)