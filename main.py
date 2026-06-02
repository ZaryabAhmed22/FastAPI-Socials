import uvicorn

if __name__ == "__main__":
    # Run the app in development mode (reload=True)
    # app.app:app >> app (package) . app (module) : app (variable)
    # host="0.0.0.0" >> Run on all available interfaces ( accesible from network)
    # port=8000 >> Run on port 8000 (standard for development)
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)