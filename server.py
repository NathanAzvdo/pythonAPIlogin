import uvicorn

def main():
    uvicorn.run(
        "loginSystem.api:app",
        host="localhost",
        port=8501,
        reload=True,
    )
    
if __name__ == "__main__":
    main()