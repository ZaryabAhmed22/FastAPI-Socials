from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse

app = FastAPI()

text_posts = {
   1: {
    "id": "1", 
    "title": "Post 1",
    "content": "Content 1"
   },
   2: {
    "id": "2",
    "title": "Post 2",
    "content": "Content 2"
   },
   3: {
    "id": "3",
    "title": "Post 3",
    "content": "Content 3"
   },
   4: {
    "id": "4",
    "title": "Post 4",
    "content": "Content 4"
   },
   5: {
    "id": "5",
    "title": "Post 5",
    "content": "Content 5"
   },
   6: {
    "id": "6",
    "title": "Post 6",
    "content": "Content 6"
   },
   7: {
    "id": "7",
    "title": "Post 7",
    "content": "Content 7"
   },
   8: {
    "id": "8",
    "title": "Post 8",
    "content": "Content 8"
   },
   9: {
    "id": "9",
    "title": "Post 9",
    "content": "Content 9"
   },
   10: {
    "id": "10",
    "title": "Post 10",
    "content": "Content 10"
   }
}

@app.get("/hello-world")
def hello_world():
    return {"message": "Hello, World!"} # JSON >> JavaScript Object Notation

# Using query params
@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

 # using path parameters    
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    if post_id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(post_id)


# We are using pydantic model to define the structure of the request body
# It will automatically validate the request body
# -> INDICATES THE RETURN TYPE OF THE FUNCTION: We can only return data in this format
@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    # post is now an object of PostCreate class
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post
