import os
import time
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from extract_text import extract_text_from_pptx
from fetch_explanation import get_explanations, save_explanations

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
STATUS_FILE = 'file_status.json'

def load_status():
    """
    Load the status of processed files from a JSON file.

    Returns:
        dict: A dictionary containing the processing status of files.
    """
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_status(status):
    """
    Save the status of processed files to a JSON file.

    Args:
        status (dict): A dictionary containing the processing status of files.
    """
    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f, indent=4)

def get_unprocessed_files(status):
    """
    Get a list of files that have not yet been processed.

    Args:
        status (dict): A dictionary containing the processing status of files.

    Returns:
        list: A list of filenames that have not been processed.
    """
    uploads = os.listdir(UPLOAD_FOLDER)
    unprocessed = []
    for upload in uploads:
        if status.get(upload) != 'processed':
            unprocessed.append(upload)
    return unprocessed

async def process_file(filename, status):
    """
    Process a file by extracting text, fetching explanations, and saving the results.

    Args:
        filename (str): The name of the file to be processed.
        status (dict): A dictionary containing the processing status of files.
    """
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    slides_texts = extract_text_from_pptx(file_path)
    explanations = await get_explanations(slides_texts)
    output_path = os.path.join(OUTPUT_FOLDER, f"{filename}.json")
    save_explanations(explanations, output_path)
    status[filename] = 'processed'
    save_status(status)
    print(f"Processed {filename}")

def main():
    """
    Main function to continuously check for and process unprocessed files.
    """
    status = load_status()
    while True:
        unprocessed_files = get_unprocessed_files(status)
        for filename in unprocessed_files:
            print(f"Processing {filename}")
            asyncio.run(process_file(filename, status))
        time.sleep(10)

if __name__ == '__main__':
    main()
