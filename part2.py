import fitz
import os

import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	

path = "/"
dir_list = os.listdir("pdf_files") 
    
name=""
for i in dir_list:
    doc = fitz.open("pdf_files/"+i)
    for page in doc:
        text = page.get_text()
        name+=text
result=""
j=0
for j in range(1,len(name),j+1000):
        
    output = query({
	    "inputs": name[j:j+1000]
        })
    result+=output[0]["summary_text"]
x,y=int(len(name)/1000)*1000,len(name)

output = query({
	"inputs": name[x:y]})
result+=output[0]["summary_text"]
print(result)
