from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["https://www.google.com", "https://www.youtube.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my API!!!"}




# my_post= [{"title": "title of post1", "content": "content of post2",
#            "id":1},{"title": "title of post2", "content": "content of post2",
#                     "id":2}]

# def find_post(id):
#     for p in my_post:
#         if p["id"] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_post):
#         if p['id'] == id:
#             return i



