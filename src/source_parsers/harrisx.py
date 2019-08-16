# SurveyUSA Parser
# - Pulls 
from bs4 import BeautifulSoup
import requests
import re
import pandas  as pd
import hashlib

class HarrisXLoader:
		
	def load(self, url):
		print(url)
		req = requests.get(url)

		soup = BeautifulSoup(req.text, 'html.parser')
		table = soup.find('table')

		for i,df in enumerate(pd.read_html(table.prettify(), flavor='bs4', header=None)):
			df.columns = range(len(df.columns))
			totals = df.iloc[1::2, :]
			totals = totals.append(df.loc[2, :], ignore_index=True)
			totals = totals.iloc[:,2:]

			geography = 'National'
			ci = 'None'
			sample = df.loc[2, 3]
			date_string = str(df.loc[0,1])
			date_collected = date_string[date_string.index('conducted ')+len('conducted '):-1]
			pollid = hashlib.md5(('SurveyUSA' + str(date_collected) + str(sample) + 'LV' + str(ci) + 'CI' + str(geography)).encode())

			totals.to_csv('../out/'+pollid.hexdigest()+'.csv', index=False, header=False)

			return {
				'PollId': str(pollid.hexdigest()),
				'Source': 'HarrisX',
				'DateCollected': str(date_collected),
				'Sample': str(sample),
				'SampleType': 'RV',
				'Error': str(ci), 
				'ErrorType': 'None',
				'Location': str(geography)
			}