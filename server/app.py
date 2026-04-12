from inference import app

def main():
    return app

# 👇 THIS IS THE MISSING PART
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.app:main", host="0.0.0.0", port=7860)