import pymongo 
import requests 






from urllib.parse import quote_plus

import os 
from dotenv import load_dotenv




# mongo credentials 
load_dotenv()


def get_required_env(name: str) -> str:
	value = os.getenv(name)
	if value is None or value.strip() == "":
		raise ValueError(f"Missing required environment variable: {name}")
	return value


USER_NAME = get_required_env("USER_NAME")
PASSWORD = get_required_env("PASSWORD")
CLUSTER_NAME = get_required_env("CLUSTER_NAME")
APP_NAME = get_required_env("APP_NAME")

user_name = quote_plus(USER_NAME)
password = quote_plus(PASSWORD)
cluster_name = quote_plus(CLUSTER_NAME)
app_name = quote_plus(APP_NAME)


mongo_uri  = "mongodb+srv://" + user_name +  ":" + password + "@" + cluster_name + "/?appName=" + app_name


client = pymongo.MongoClient(mongo_uri)
db = client.sample_mflix 
collection = db.movies 




HUGGING_FACE_TOKEN=get_required_env("HUGGING_FACE_TOKEN")
# endpoint to the hf server to compute embeddings
# all-MiniLM-L6-v2 is registered as sentence-similarity on HF, not feature-extraction,
# so we use BAAI/bge-small-en-v1.5 which is tagged as feature-extraction and is equivalent in size/quality.
EMBEDDING_URL="https://router.huggingface.co/hf-inference/models/BAAI/bge-small-en-v1.5"



def generate_embedding(text: str) -> list[float]:
	response = requests.post(
		EMBEDDING_URL,
		headers={
			"Authorization": f"Bearer {HUGGING_FACE_TOKEN}",
		},
		json={"inputs": text},
	)

	if response.status_code != 200:
		raise ValueError(
			f"Request failed with status code {response.status_code}: {response.text}"
		)

	data = response.json()
	# The Inference API returns [[float, ...]] for a single input — unwrap it
	if isinstance(data, list) and data and isinstance(data[0], list):
		return data[0]
	return data









# print(f"Testing: {mongo_uri}")
# print(collection.find().limit(5))
# items = collection.find().limit(5)


# for item in items:
# 	print(item)
# print(generate_embedding("freeCodeCamp is awesome"))

# test_documents = collection.find({"plot": {"$exists": True}}).limit(50)
# for doc in test_documents:
# 	doc["plot_embedding_hf"] = generate_embedding(doc["plot"])
# 	collection.replace_one({
# 		"_id": doc["_id"]
# 	}, 	doc) # replaces existing doc with _id with the new one (with a new field)
# 	print("Completed")

# print("Done!!")


# 
query = "imaginary characters from outer space at war"
print(f"Given the query: {query}")
# used to find documents in a collection where the following constraint holds:
# the field "plot_embedding_hf" is semantically similar to the provided `query`
results = collection.aggregate([
	{
		"$vectorSearch": {
			"queryVector": generate_embedding(query), # generat the embedding for the query string 
			"path": "plot_embedding_hf",
			"numCandidates": 100, # how many candidates matched internally before returning results.
			"limit": 4,			  # limit the number of results.
			"index": "PlotSemanticSearch",
		}
	}
])

# print("starting")

# print(f"results = {results}")
for document in results:
	print("--- completed ---")
	print(f"Movie Name: {document["title"]},\nMovie plot: {document["plot"]}\n")