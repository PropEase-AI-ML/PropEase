import csv
import json
import os
from typing import List

import llama_cpp


def load_model(model_path, n_ctx=4096, n_batch=512, n_threads=10):
    """
    Load a GGUF model using llama.cpp
    
    :param model_path: Path to the GGUF model file
    :return: Loaded llama.cpp model
    """
    try:
        model = llama_cpp.Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_batch=n_batch,
            n_threads=n_threads,
            n_gpu_layers=-1
        )
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def read_prompt_template(file_path):
    """
    Read prompt template from a text file
    
    :param file_path: Path to the prompt template file
    :return: Prompt template as a string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading prompt template: {e}")
        return None
    
def loop_txt_files(folder_path: str) -> List[str]:
    """
    Loops over txt files in the specified folder.
    
    Args:
        folder_path (str): Path to the folder containing txt files
    
    Returns:
        List[str]: List of full paths to txt files in the folder
    """
    # List to store txt file paths
    txt_files = []
    
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist.")
        return txt_files
    
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a txt file
        if filename.lower().endswith('.txt'):
            # Create full file path
            full_path = os.path.join(folder_path, filename)
            txt_files.append(full_path)
            print(f"Found txt: {filename}")
    
    return txt_files

def read_file_content(file_path: str) -> str:
    """
    Safely read file content with multiple parsing attempts
    
    :param file_path: Path to the input file
    :return: Parsed content as a string
    """
    try:
        # Try reading as plain text
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
        
        # If content looks like JSON, try parsing
        if content.startswith('{') and content.endswith('}'):
            try:
                # Try parsing as JSON
                parsed_content = json.loads(content)
                # Convert back to a readable string representation
                return json.dumps(parsed_content, indent=2)
            except json.JSONDecodeError:
                # If JSON parsing fails, return original content
                return content
        
        return content
    
    except UnicodeDecodeError:
        # Try reading with different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    return file.read().strip()
            except Exception:
                continue
        
        print(f"Could not read file {file_path} with any encoding")
        return ""
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def run_inference(model, prompt, max_tokens=300, temperature=0.7):
    """
    Run inference on the loaded model
    
    :param model: Loaded llama.cpp model
    :param prompt: Input prompt for generation
    :return: Generated text
    """
    try:
        output = model(
            prompt, 
            max_tokens=max_tokens, 
            temperature=temperature,
            top_p=0.95,
            top_k=40,
            repeat_penalty=1.1,
        )
        return output['choices'][0]['text']
    except Exception as e:
        print(f"Error during inference: {e}")
        return None

def save_results_to_csv(results_list, output_path):
    """
    Save results to a CSV file
    
    :param results_list: List of tuples (document_path, llm_answer)
    :param output_path: Path to the output CSV file
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Open the file in write mode
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            # Create a CSV writer object
            csv_writer = csv.writer(csvfile)
            
            # Write header
            csv_writer.writerow(['Document Path', 'LLM Answer'])
            
            # Write results
            for result in results_list:
                csv_writer.writerow(result)
        
        print(f"Results saved to {output_path}")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")

def main():
    # Model path
    model_path = "local/Mistral-7B-Instruct-v0.2-Code-FT.gguf"
    
    # Prompt template path
    template_path = "prompts/classifier.txt"
    
    # Types placeholder
    types = ["Asbestos", "EPC", "other"]

    # Variable to replace placeholder
    txt_data = loop_txt_files("local/data")
    
    # List to store results
    results = []
    
    # Load model
    model = load_model(model_path)
    
    if model:
        # Read prompt template
        prompt_template = read_prompt_template(template_path)
        
        if prompt_template:
            for txt in txt_data:
                print(f"Processing file: {txt}")
                
                # Read file content with robust method
                input_variable = read_file_content(txt)
                
                if input_variable:
                    try:
                        # Replace placeholder with input variable
                        filled_prompt = prompt_template.replace("{TYPES}", ", ".join(types))
                        filled_prompt = filled_prompt.replace("{INPUT_REPORT}", input_variable)
                        
                        print("Full Prompt:")
                        print(filled_prompt)
                        
                        # Run inference
                        response = run_inference(model, filled_prompt)
                        
                        if response:
                            print("\nModel Response:")
                            print(response)
                            
                            # Add result to the list
                            results.append((txt, response))
                    
                    except Exception as e:
                        print(f"Error processing {txt}: {e}")
                else:
                    print(f"Could not read content from {txt}")
            
            # Save results to CSV
            save_results_to_csv(results, "local/llm_results.csv")

if __name__ == "__main__":
    main()