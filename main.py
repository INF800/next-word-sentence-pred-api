# ----------------------------------------
# create fastapi app 
# ----------------------------------------
from fastapi import FastAPI
app = FastAPI()


# ----------------------------------------
# setup templates folder
# ----------------------------------------
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")


# ----------------------------------------
# setup db
# ----------------------------------------
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine) #creates tables
# stocks db will appear once you run uvicorn.
# get into sqlite and try `.schema`


# ----------------------------------------
# import custom modules
# ----------------------------------------
from tree.Tree import tree, words

# ----------------------------------------
# dependency injection
# ----------------------------------------
from fastapi import Depends

def get_db():
	""" returns db session """
	
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close


# ----------------------------------------
# bg tasks
# ----------------------------------------
from fastapi import BackgroundTasks

def fetch_real_time(pk: int):
	pass


# ----------------------------------------
# define structure for requests (Pydantic & more)
# ----------------------------------------
from fastapi import Request # for get
from pydantic import BaseModel # for post

class QueryRequest(BaseModel):
	incomplete_word: str


# ----------------------------------------
# Cross Origin Resource Sharing
# ----------------------------------------


# ----------------------------------------
# ----------------------------------------
# routes and related funcs
# ----------------------------------------
# ----------------------------------------
@app.get("/")
def api_home(request: Request):
	"""
	home page to display all real time values
	"""
	
	context = {
		"request": request
	}
	return templates.TemplateResponse("index.html", context)

@app.get("/api/{incomplete_word}")
def api_home(request: Request, incomplete_word):
	"""
	process incomplete word and send {"response": "complete word"}
	"""
	# 1. search the rank of quer string in tree 
	# (rank is stored in self.q_rank[0]) 
	tree.q_rank = None
	tree.search(incomplete_word)

	# 2. based on rank, get suggestion from pop sorted list of words
	# where index is rank
	suggestion = ""
	# 3. `incomplete_word[-1]==tree.q_rank[1]`:
	# 	 Make sure your incompleteword and tree search end with same word
	# 	 otherwise, `epson` will be given for both `eps` & `epsi`
	# 	 (This can be awesome suggestion feature though) 
	if tree.q_rank[0] is not None and incomplete_word[-1]==tree.q_rank[1]:
		suggestion = words[tree.q_rank[0]]
	return {"response":suggestion}