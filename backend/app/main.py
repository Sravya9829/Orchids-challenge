from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import clone

app = FastAPI(title="Website Cloner API", version="1.0.0")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the clone router
app.include_router(clone.router)

@app.get("/")
def read_root():
    return {"message": "Website Cloner API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "website-cloner"}