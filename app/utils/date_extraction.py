# import re
# import spacy
# from langdetect import detect
# import dateparser

# nlp_fr = spacy.load("fr_core_news_sm")
# nlp_nl = spacy.load("nl_core_news_sm")

# DATE_REGEX = r"\b(\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4}|\d{1,2}\s(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s\d{4})\b"

# def extract_dates(text):
#     lang = detect(text)
#     nlp = nlp_fr if lang == 'fr' else nlp_nl if lang == 'nl' else None
    
#     if not nlp:
#         return "No date found"
    
#     doc = nlp(text)
#     extracted_dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
#     regex_dates = re.findall(DATE_REGEX, text)
    
#     all_dates = extracted_dates + regex_dates
    
#     parsed_dates = []
#     for date in all_dates:
#         parsed = dateparser.parse(date, languages=[lang])
#         if parsed:
#             parsed_dates.append(parsed.strftime("%Y-%m-%d"))

#     return max(parsed_dates) if parsed_dates else "No date found"

import re
import spacy
from langdetect import detect
import dateparser
from datetime import datetime
from dateutil import parser
import datefinder

# Load spaCy models for multiple languages
nlp_fr = spacy.load("fr_core_news_sm")
nlp_nl = spacy.load("nl_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")  # English support

# Enhanced date regex (supports more formats)
DATE_REGEX = r"""
\b(\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4} |                            # 01-01-2024 or 1/1/24
   \d{4}[\/\-.]\d{1,2}[\/\-.]\d{1,2} |                               # 2024-01-01
   \d{1,2}\s(?:janvier|février|mars|avril|mai|juin|                  # 1 janvier 2024
   juillet|août|septembre|octobre|novembre|décembre)\s\d{4} |        # French full dates
   \d{1,2}(?:st|nd|rd|th)?\s(?:January|February|March|April|May|     # English ordinal dates
   June|July|August|September|October|November|December)\s\d{4})\b   # English full dates
"""

# Compile regex for performance
DATE_REGEX = re.compile(DATE_REGEX, re.VERBOSE | re.IGNORECASE)

def extract_dates(text):

    # dateparser
    lang = detect(text)
    
    # Choose spaCy model based on detected language
    nlp = {
        'fr': nlp_fr,
        'nl': nlp_nl,
        'en': nlp_en
    }.get(lang, None)
    
    if not nlp:
        matches = list(datefinder.find_dates(text))
    
        if matches:
            # Return all detected dates
            return [date.strftime("%Y-%m-%d") for date in matches][0]
        
        return "No date found"

    # 1. NER (Named Entity Recognition) Date Extraction
    doc = nlp(text)
    extracted_dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    
    # 2. Regex-Based Date Extraction
    regex_dates = DATE_REGEX.findall(text)
    
    # Combine all detected dates
    all_dates = extracted_dates + regex_dates
    
    parsed_dates = []
    
    for date in all_dates:
        # Try parsing with dateparser
        parsed = dateparser.parse(date, languages=[lang])
        if not parsed:
            try:
                parsed = parser.parse(date, fuzzy=True)  # Fallback to dateutil
            except:
                continue
        
        if parsed:
            parsed_dates.append(parsed.strftime("%Y-%m-%d"))
    
    if not parsed_dates:
        matches = list(datefinder.find_dates(text))
    
        if matches:
            # Return all detected dates
            return [date.strftime("%Y-%m-%d") for date in matches][0]

    # Return the most recent date (or all if needed)
    return parsed_dates[0] if parsed_dates else "No date found"
