# SurveyUSA Parser
# - Pulls
import re
import pandas  as pd
from PyPDF2 import PdfFileReader
import hashlib

class YouGovLoader:
		
	def load(self, pdf):
		# better way to do this, should be in same function, because reloading pdf
		survey_start = self.find_page_range(pdf, 'IftheDemocraticpresidentialprimaryorcaucusinyourstatewereheldtoday,whowouldyouvotefor?')
		survey_end = self.find_page_range(pdf, 'ArethereanypresidentialcandidatesthatyouwouldbedisappointediftheybecametheDemocraticnominee?')

		print(survey_start)
		print(survey_end)

		sample = 0
		ci = 0
		date_collected = 0
		geography = 0

		pollid = hashlib.md5(('SurveyUSA' + str(date_collected) + str(sample) + 'LV' + str(ci) + 'CI' + str(geography)).encode())

		#df.to_csv('../out/'+pollid.hexdigest()+'.csv', index=False, header=False)

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
	
	def find_page_range(self, f, str):
		pages = []
		pdfDoc = PdfFileReader('../data/YouGov/'+f)
		for i in range(0, pdfDoc.getNumPages()):
			page = pdfDoc.getPage(i)
			txt = page.extractText()
			print(txt)
			search = re.search(str, txt)
			if search is not None:
				pages.append(i)
				break
		
		return pages