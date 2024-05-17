import uvicorn

def main():
    uvicorn.run(
        "app.api:app",
        host="localhost",
        port=8503,
        reload=True,
    )
    
if __name__ == "__main__":
    main()