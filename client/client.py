import requests
import os
import argparse
from datetime import datetime
import time

class Status:
    """
    Represents the status of a file processing operation.
    
    Attributes:
        status (str): The processing status ('pending' or 'done').
        filename (str): The original filename of the uploaded file.
        timestamp (datetime): The timestamp when the file was uploaded.
        explanation (str): The explanation generated for the file.
    """
    def __init__(self, status, filename, timestamp, explanation):
        self.status = status
        self.filename = filename
        self.timestamp = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        self.explanation = explanation

    def is_done(self):
        """
        Check if the processing is complete.
        
        Returns:
            bool: True if processing is done, False otherwise.
        """
        return self.status == 'done'

class Client:
    """
    Client for interacting with the Flask web API to upload .pptx files and check their processing status.
    
    Attributes:
        base_url (str): The base URL of the Flask web API.
    """
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        """
        Upload a .pptx file to the web API.
        
        Args:
            file_path (str): The path to the .pptx file to be uploaded.
        
        Returns:
            str: The unique identifier (UID) of the uploaded file.
        
        Raises:
            requests.exceptions.RequestException: If the upload request fails.
        """
        with open(file_path, 'rb') as f:
            response = requests.post(f"{self.base_url}/upload", files={'file': f})
        if response.status_code == 200:
            return response.json()['uid']
        else:
            response.raise_for_status()

    def check_status(self, uid):
        """
        Check the processing status of an uploaded file.
        
        Args:
            uid (str): The unique identifier (UID) of the uploaded file.
        
        Returns:
            Status: An instance of the Status class containing the file's processing status and explanation.
        
        Raises:
            requests.exceptions.RequestException: If the status request fails.
        """
        response = requests.get(f"{self.base_url}/status/{uid}")
        if response.status_code == 200:
            data = response.json()
            return Status(data['status'], data['filename'], data['timestamp'], data['explanation'])
        else:
            response.raise_for_status()

def main():
    """
    Main function to handle command-line arguments and execute the appropriate client actions.
    """
    parser = argparse.ArgumentParser(description="Client for uploading .pptx files and checking status")
    parser.add_argument('command', choices=['upload', 'status'], help="Command to execute")
    parser.add_argument('path', type=str, help="Path to the .pptx file or UID to check status")

    args = parser.parse_args()
    client = Client("http://localhost:5000")

    if args.command == 'upload':
        uid = client.upload(args.path)
        print(f"Uploaded file UID: {uid}")
    elif args.command == 'status':
        uid = args.path
        for _ in range(10):  # Check status periodically
            status = client.check_status(uid)
            print(f"File status: {status.status}")
            if status.is_done():
                print(f"Explanation: {status.explanation}")
                break
            time.sleep(5)
        else:
            print("File was not processed in time")

if __name__ == "__main__":
    main()
