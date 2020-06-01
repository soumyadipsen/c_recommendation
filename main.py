import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

import pandas as pd
import sys
app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))





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
	output=customer_recomendation(n)
	if(type(output)==type('string')):
		return render_template('index.html', prediction_text='Customer Not Found')
	else:
		o=""
		o=o+output[0]
		output=o.split("|")
		print(output)
		return render_template('index.html', prediction_text='Recommended Products are: {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)