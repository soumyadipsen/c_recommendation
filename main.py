import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import csv
import pandas as pd
import sys
app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))


prod="product.csv"



def customer_recomendation(customer_id):
	user_id = 'customerId'
	item_id = 'productId'
	model['recommendedProducts'] = model.groupby([user_id])[item_id].transform(lambda x: '|'.join(x.astype(str)))
	df_output = model[['customerId', 'recommendedProducts']].drop_duplicates().sort_values('customerId').set_index('customerId')

	if customer_id not in df_output.index:
		print('Customer not found.')
		return('Customer not found.')
	return df_output.loc[customer_id]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend')
def recommend():
	
	
	n = request.args.get('n')
	n=int(n)
	f=[]
	r=[]
	output=customer_recomendation(n)
	if(type(output)==type('string')):
		return render_template('index.html', pt1='Customer Not Found')
	else:
		o=""
		o=o+output[0]
		output=o.split("|")
		print(output)
		pt=[]
		xyz=[]
		with open(prod,'r') as csvfile:
			csvreader=csv.reader(csvfile)
			f=next(csvreader)
			for rows in csvreader:
				xyz.append(rows)
		for ii in range(10):
			for row in xyz:
				if (output[ii] == row[0]):
					pt.append(row[1])
		print(pt)
		return render_template('index.html',pt=pt)


if __name__ == "__main__":
    app.run(debug=True)