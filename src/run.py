from source_parsers.surveyusa import SurveyUSALoader
from source_parsers.harrisx import HarrisXLoader
from source_parsers.yougov import YouGovLoader
import pandas as pd
import os

def main():

    df = pd.DataFrame(columns=['PollId', 'Source', 'DateCollected', 'Sample', 'SampleType', 'Error', 'ErrorType', 'Location'])
    hx = HarrisXLoader()
    susa = SurveyUSALoader()
    yg = YouGovLoader()

    """     with open("../data/SurveyUSA/sources.csv", "r") as ins:
        array = []
        for line in ins:
            susa = SurveyUSALoader()
            poll = susa.load(line.strip())
            df = df.append(poll, ignore_index=True)
            print(poll)
    

    with open("../data/HarrisX/sources.csv", "r") as ins:
        array = []
        for line in ins:
            poll = hx.load(line.strip())
            df = df.append(poll, ignore_index=True)
            print(poll) """
    
    for file in os.listdir('../data/YouGov'):
        if file.endswith('.pdf'):
            poll = yg.load(file)
            print(poll)


    print(df)
    df.to_csv('../out/poll_list.csv', index=False)


if  __name__ =='__main__':
    main()
