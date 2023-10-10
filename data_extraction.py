import nltk
import json
from nltk.tokenize import sent_tokenize
import pandas as pd
import spacy
from spacy.matcher import Matcher, PhraseMatcher

def extract_sentences_with_metrics(text_data):
    # input is a string of text data
    # output is a dataframe with two columns: Sentence and Metric

    # Load the spaCy language model
    nlp = spacy.load('en_core_web_sm')

    # Define custom spaCy matchers for financial metrics

    # Revenue Matcher
    revenue_matcher = Matcher(nlp.vocab)
    revenue_matcher.add("revenue_match", [[{'LOWER': {'IN': ['income', 'proceeds', 'takings', 'receipts', 'sales', 'turnover']}}]])

    # Net Income Matcher
    net_income_matcher = PhraseMatcher(nlp.vocab)
    net_income_patterns = [nlp(text) for text in ('net income', 'profit', 'profits','profitability','earnings', 'bottom line')]
    net_income_matcher.add("net_income_match", None, *net_income_patterns)

    # EBIT Matcher
    ebit_matcher = PhraseMatcher(nlp.vocab)
    ebit_patterns = [nlp(text) for text in ('ebit', 'earnings before interest and taxes', 'operating profit', 'operating profits', 'operating income')]
    ebit_matcher.add("ebit_match", None, *ebit_patterns)

    # EPS Matcher
    eps_matcher = PhraseMatcher(nlp.vocab)
    eps_patterns = [nlp(text) for text in ('eps', 'earnings per share')]
    eps_matcher.add("eps_match", None, *eps_patterns)

    # Cash Flow Matchers
    cash_flow_matcher = Matcher(nlp.vocab)
    operating_patterns = [
        {'LOWER': {'in': ['cash', 'flow']}},
        {'LEMMA': {'in': ['operate','operation']}},
    ]

    operating_patterns1 = [
        {'LOWER': {'in': ['cffo','cfo']}},
    ]

    investing_patterns = [
        {'LOWER': {'in': ['cash', 'flow']}},
        {'LEMMA': {'in': ['invest','investment']}},
    ]

    financing_patterns = [
        {'LOWER': {'in': ['cash', 'flow']}},
        {'LEMMA': {'in': ['finance', 'funding']}},
    ]


    cash_flow_matcher.add("operating_match", [operating_patterns])
    cash_flow_matcher.add("operating_match1", [operating_patterns1])
    cash_flow_matcher.add("investing_match", [investing_patterns])
    cash_flow_matcher.add("financing_match", [financing_patterns])

    
    # Define a mapping of matchers to metric names
    matcher_to_metric = {
        revenue_matcher: "Revenue",
        net_income_matcher: "Net Income",
        ebit_matcher: "EBIT",
        eps_matcher: "EPS",
        cash_flow_matcher: "Cash Flow"
    }

    # Initialize nlp object and list for storing matches
    nlp_doc = nlp(text_data)
    sentences_metrics = []
    
    # Split the text into sentences
    sentences = [sentence.text for sentence in nlp_doc.sents]

    # Iterate through each sentence
    for sentence in sentences:
        doc = nlp(sentence)
        matched_metrics = set() # Initialize set for storing matched metrics to avoid duplicates
        # Check for financial metrics matches
        for matcher, metric_name in matcher_to_metric.items():
            matches = matcher(doc)
            if matches:
                for match_id, start, end in matches:
                    if matcher == cash_flow_matcher:
                        for match_id, start, end in matches:
                            if nlp.vocab.strings[match_id] == "operating_match":
                                matched_metrics.add('Cash Flow (Operating)')
                            elif nlp.vocab.strings[match_id] == "operating_match1":
                                matched_metrics.add('Cash Flow (Operating)')
                            elif nlp.vocab.strings[match_id] == "investing_match":
                                matched_metrics.add('Cash Flow (Investing)')
                            elif nlp.vocab.strings[match_id] == "financing_match":
                                matched_metrics.add('Cash Flow (Financing)')
                    else: matched_metrics.add(metric_name)
        # Append the sentence with matched metrics to the result list
        for matched_metric in matched_metrics:
            sentences_metrics.append({'Sentence': sentence, 'Metric': matched_metric})

    # Create a DataFrame with combined results
    sentences_metrics_df = pd.DataFrame(sentences_metrics)
    
    return sentences_metrics_df 

def clean_newlines(sentence_list):
    #takes list as input and gives list as output
    #cleans unnecesary linebreaks etc.
    
    
    for q in range(len(sentence_list)):
        sentence_list[q] = sentence_list[q].strip() 
        sentence_list[q] = sentence_list[q].replace('\n', ' ') 
        sentence_list[q] = sentence_list[q].replace('\r', '') 
        sentence_list[q] = sentence_list[q].replace(' ', ' ') 
        sentence_list[q] = sentence_list[q].replace(' ', ' ')
        sentence_list[q] = sentence_list[q].replace('\xa0',' ')
        sentence_list[q] = sentence_list[q].replace('&nbsp;',' ')
        sentence_list[q] = sentence_list[q].replace('&#160;',' ')
        while '  ' in sentence_list[q]:
            sentence_list[q] = sentence_list[q].replace('  ',' ')
        
    return sentence_list


def categorize_fls(sentence,date):
    #performs rule-based-matching
    #takes a sentence and a year as input and returns individual sentences that contain a match
    
    # Load the spaCy language model
    nlp = spacy.load('en_core_web_sm')
    
    #initialize as nlp object and prepare list for storing matches
    sen = nlp(sentence)
       
    #two seperate matchers, so that pattern 3 can be checked separately 
    matcher = Matcher(nlp.vocab)
    matcher2 = Matcher(nlp.vocab)
    pattern1 =  [{"TEXT": {"IN": ["next", "subsequent", "following", "upcoming", "incoming", "coming", "succeeding", "carryforward"]}},
            {"TEXT": {"IN": ["month", "quarter", "year", "fiscal", "taxable", "period"]}}]
    pattern2 = [{"LEMMA": {"IN": ["aim", "anticipate", "assume", "commit", "estimate", "expect", "forecast", "foresee", "hope", "intend", "plan", "predict", "project", "seek","target"]},"POS": "VERB"}]
    pattern3 = [{"TEXT": {"REGEX": "[1-2][0-9][0-9][0-9]"}, "LENGTH": 4}]
    matcher.add('pattern1',[pattern1])
    matcher.add('pattern2',[pattern2])
    matcher2.add('pattern3',[pattern3])
    
    #if patterns were found in a sentence, append it to the list
    
    if matcher(sen) != []:
        return "FLS"
        
    #if no matches for patterns 1 or 2 are found, check matches for pattern 3 and check if they are higher than the year provided as input.
    elif matcher2(sen) != []:
        years=[]
        for match_id, start, end in matcher2(sen):
            years.append(int(sen[start:end].text))
        if max(years) > date:
            return "FLS"
    return "Non-FLS"


def extract_sentences_complete(data):
    # input is a dataframe converted from 10-K filings in JSON format
    # output is a dataframe including the original data 
    # and the extracted sentences, the corresponding metrics and FLS classification
    
    results = []
    items = ['item_1A', 'item_7', 'item_7A']
    for item in items:
        fls_with_metrics_item = pd.DataFrame(columns=['Sentence', 'Metric'])
        for index,row in data.iterrows():
            # extract sentences with metrics from the current row
            sentences_with_metrics = extract_sentences_with_metrics(row[item])
            if sentences_with_metrics.empty:
                continue
            sentences_with_metrics_clean = clean_newlines(sentences_with_metrics['Sentence'])
            sentences_with_metrics['Sentence'] = sentences_with_metrics_clean
            
            # create a dataframe with the current row's data
            sentences_with_metrics['Item'] = item 
            sentences_with_metrics['Year'] = row['year']
            sentences_with_metrics['CIK'] = row['cik']
            sentences_with_metrics['Company'] = row['company']
            
            # append the result for the current row to the item's result DataFrame
            fls_with_metrics_item = pd.concat([fls_with_metrics_item, sentences_with_metrics], ignore_index=True)

        # apply categorize_fls function to the dataframe
        fls_with_metrics_item['FLS'] = fls_with_metrics_item.apply(
            lambda x: categorize_fls(x['Sentence'], x['Year']), axis=1
            )
        # append the result for the current row to the item's result DataFrame
        results.append(fls_with_metrics_item)

        # print progress
        print(f"Finished extracting sentences for {item}")

    # concatenate all dataframes in the list
    fls_with_metrics = pd.concat(results, ignore_index=True)

    # drop possible duplicates
    fls_with_metrics.drop_duplicates(inplace=True)
    return fls_with_metrics