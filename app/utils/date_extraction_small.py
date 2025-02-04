import re
import dateparser

# --- Extended Expiry Keywords for French and Dutch ---

# French keywords (including variations, synonyms, and common abbreviations)
expiry_keywords_fr = [
    "valide jusqu",            # e.g., "valide jusqu'au", "valide jusqu’à"
    "valable jusqu",           # e.g., "valable jusqu'à", "valable jusqu’à"
    "date limite",             # e.g., "date limite de"
    "d'expiration",            # e.g., "date d'expiration"
    "date d'expiration",       # explicit full phrase
    "expiration",              # just the root word
    "validité maximale",       # e.g., "Validité maximale :"
    "échéance",                # e.g., "échéance", "date d'échéance"
    "fin de validité",         # e.g., "fin de validité"
    "date de péremption",      # sometimes used
    "péremption",              # short version
    "date de fin",             # e.g., "date de fin de"
    "terme de validité",       # a less common variant
    "arrêt de validité",       # sometimes used to indicate end of validity
    "expire le",               # e.g., "expire le 15/09/2031"
]

# Dutch keywords (including common variations and synonyms)
expiry_keywords_nl = [
    "geldig tot",             # e.g., "Geldig tot :", "geldig tot en met"
    "verval",                 # covers "vervalt", "vervallen"
    "vervaldatum",            # explicit keyword
    "houdbaar tot",           # e.g., "houdbaar tot"
    "uiterste gebruiksdatum", # longer phrase sometimes seen
    "einddatum",              # e.g., "einddatum"
    "datum einde",            # variation on end date
    "geldigheidsdatum",       # sometimes used
    "verloopt op",            # e.g., "verloopt op 27/06/2032"
    "afloopdatum",            # similar to einddatum
    "eindigt op",             # variation indicating termination
    "eindigt",                # abbreviated form
]

# Combine all keywords and convert them to lowercase for easier matching
expiry_keywords = [kw.lower() for kw in expiry_keywords_fr + expiry_keywords_nl]

# --- Regex Patterns to Match Date Candidates ---
regex_patterns = [
    # Numeric dates: e.g., dd/mm/yyyy, dd-mm-yyyy, or d/m/yy
    r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',

    # Textual dates with French month names (e.g., "15 juin 2025")
    r'\b\d{1,2}\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b',

    # Textual dates with Dutch month names (e.g., "6 juni 2025")
    r'\b\d{1,2}\s+(januari|februari|maart|april|mei|juni|juli|augustus|september|oktober|november|december)\s+\d{4}\b',

    # Month-first textual dates, e.g., "juin 6, 2025" or "juni 6 2025"
    r'\b(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{1,2}(?:,\s*\d{4})?\b',
    r'\b(januari|februari|maart|april|mei|juni|juli|augustus|september|oktober|november|december)\s+\d{1,2}(?:,\s*\d{4})?\b'
]

# --- Helper Functions ---

def has_expiry_context(text, match_start, match_end, window=80):
    """
    Check if the context around a found date candidate contains any expiry-related keywords.
    
    Parameters:
      text (str): The full text.
      match_start (int): Start index of the date candidate.
      match_end (int): End index of the date candidate.
      window (int): Number of characters before and after to consider.
    
    Returns:
      bool: True if any expiry keyword is found, False otherwise.
    """
    start = max(0, match_start - window)
    end = min(len(text), match_end + window)
    context = text[start:end].lower()
    return any(kw in context for kw in expiry_keywords)

def extract_expiry_dates(text, window=80):
    """
    Extract expiry dates from a given text using regex and a context filter.
    
    Parameters:
      text (str): Input text containing date candidates.
      window (int): Character window size to check for expiry keywords.
    
    Returns:
      list: A list of expiry dates as datetime.date objects.
    """
    if not isinstance(text, str):
        return []
    extracted_dates = set()
    for pattern in regex_patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            candidate = match.group(0)
            # Only keep candidate if an expiry keyword is nearby
            if not has_expiry_context(text, match.start(), match.end(), window):
                continue
            parsed_date = dateparser.parse(candidate, languages=['fr', 'nl'])
            if parsed_date:
                extracted_dates.add(parsed_date.date())
    if extracted_dates:
        # Return the latest (biggest) date
        return max(extracted_dates)
    else:
        return "Not found"
            