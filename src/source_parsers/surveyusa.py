# SurveyUSA Parser
# - Pulls 
from bs4 import BeautifulSoup
import requests
import re
import pandas  as pd
import hashlib

class SurveyUSALoader:
		
	def load(self, url):
		
		req = requests.get(url)

		soup = BeautifulSoup(req.text, 'html.parser')

		print(url)

		report_url = 'http://www.surveyusa.com/client/' + soup.frameset.find('frame', {'name':'mainFrame'})['src']
		info_url = 'http://www.surveyusa.com/client/' + soup.frameset.find('frame', {'name':'leftFrame'})['src']

		leftReq = requests.get(info_url)
		leftSoup = BeautifulSoup(leftReq.text, 'html.parser')
		date_collected = leftSoup.find('span', id='LabelDateCollected').text
		geography = leftSoup.find('span', id='LabelGeography').text


		mainReq = requests.get(report_url + '&d=1')
		mainSoup = BeautifulSoup(mainReq.text, 'html.parser')
		tbhead = mainSoup.find('td', text='If there were a Democratic primary for President of the United States today where you live, which Democrat would you vote for? [Candidate names not shown to respondents in order displayed here.]')
		table = tbhead.parent.parent.next_sibling.next_sibling

		for i,df in enumerate(pd.read_html(table.prettify(), flavor='bs4')):
			sample = self.extract_number(df.loc[0,0])[0]
			ci = self.extract_number(df.loc[1,0])[0]

			df.loc[1,:] = df.loc[1,:].shift(1)
			df.loc[1,0] = "Candidates"
			df.loc[1,1] = "All"

			df = df.drop(0, axis=0)
			df.drop(df.index[len(df)-1])

			pollid = hashlib.md5(('SurveyUSA' + str(date_collected) + str(sample) + 'LV' + str(ci) + 'CI' + str(geography)).encode())

			df.to_csv('../out/'+pollid.hexdigest()+'.csv', index=False, header=False)

			return {
				'PollId': str(pollid.hexdigest()),
				'Source': 'SurveyUSA',
				'DateCollected': str(date_collected),
				'Sample': str(sample),
				'SampleType': 'LV',
				'Error': str(ci), 
				'ErrorType': 'CI',
				'Location': str(geography)
			}
	
	def extract_number(self, s):
		l = []
		for t in s.split():
			try:
				l.append(float(t))
			except ValueError:
				pass

		return l