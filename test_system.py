import subprocess
import pytest
import time
from client.client import Client

def start_process(command):
    """
    Start a subprocess with the given command.
    
    Args:
        command (list): The command to run as a subprocess.
    
    Returns:
        subprocess.Popen: The Popen object for the started subprocess.
    """
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def test_system():
    """
    System test that starts the web API and explainer, uploads a file, and checks its processing status.
    
    The test:
    1. Starts the Flask web API.
    2. Starts the explainer script.
    3. Uses the client to upload a PowerPoint file.
    4. Periodically checks the processing status of the uploaded file.
    5. Asserts that the file is processed within the given time and an explanation is generated.
    """
    
    api_process = start_process(['python', 'api/api.py'])
    time.sleep(5)  

    
    explainer_process = start_process(['python', 'explainer/explainer.py'])
    time.sleep(5)  

    try:
        client = Client("http://localhost:5000")
        uid = client.upload("minstack.pptx")
        assert uid is not None, "Failed to upload file"

        
        for _ in range(20):  
            status = client.check_status(uid)
            print(f"Status response: {status.status}")
            if status.is_done():
                print(f"Explanation: {status.explanation}")
                break
            time.sleep(10)  
        else:
            assert False, "File was not processed in time"

        assert status.explanation is not None, "Explanation was not generated"
    finally:
        api_process.terminate()
        explainer_process.terminate()

if __name__ == "__main__":
    pytest.main()
