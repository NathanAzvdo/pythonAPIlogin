import uvicorn

def main():
    uvicorn.run(
        "loginSystem.api:app",
        host="localhost",
        port=8500,
        reload=True,
    )
    
if __name__ == "__main__":
    main()