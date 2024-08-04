from flask import *
import fitz
import os
import requests
app = Flask(__name__) 

def summary():
	

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
		doc.close()
	result=""
	j=0
	for j in range(0,len(name),j+1000):
			
		output = query({
			"inputs": name[j:j+1000]
			})
		result+=output[0]["summary_text"]
	x,y=int(len(name)/1000)*1000,len(name)

	output = query({
		"inputs": name[x:y]})
	result+=output[0]["summary_text"]
	path = "/"
	dir_list = os.listdir("pdf_files") 

	for i in dir_list:
		os.remove("pdf_files/"+i)
	return result

@app.route('/') 
def main(): 
	return render_template("index.html") 


@app.route('/upload', methods=['GET','POST']) 
def upload(): 
	if request.method == 'POST': 

		# Get the list of files from webpage 
		files = request.files.getlist("file") 

		# Iterate for each file in the files List, and Save them 
		for file in files: 
			file.save("pdf_files/"+file.filename) 
		txt=summary()
		return txt


if __name__ == '__main__': 
	app.run(debug=True) 
