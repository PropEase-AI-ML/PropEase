from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Load Model and Tokenizer (Phi-2 by Microsoft)
# model_name = "microsoft/phi-2"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)

def llm_extract_dates(text):
    prompt = f"""
    Extract all relevant dates from the following text:
    {text}

    Return the result in JSON format with 'expiring_date'.
    If no date is found, return 'null'.
    """

    # Setup Pipeline
    phi_pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    result = phi_pipe(prompt, max_length=200)
    return result[0]['generated_text']
