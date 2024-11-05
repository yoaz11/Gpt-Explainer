# PPTX Explainer System

This project provides a system for uploading PowerPoint (.pptx) files, processing them to extract text and generate explanations using OpenAI's GPT-3.5, and checking the status of the processing. The system consists of a Flask web API, an asynchronous explainer script, and a client for interacting with the API.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Starting the Flask API](#starting-the-flask-api)
  - [Running the Explainer Script](#running-the-explainer-script)
  - [Using the Client](#using-the-client)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Upload PowerPoint (.pptx) files via a web API
- Extract text from each slide in the PowerPoint file
- Generate explanations for each slide's text using OpenAI's GPT-3.5
- Check the processing status of uploaded files

## Prerequisites

- Python 3
- OpenAI API key

## Installation

1. Clone the repository:
   git clone https://github.com/Scaleup-Excellenteam/final-exercise-yoaz11/tree/gpt-slides-Client
   
Install the required packages:
pip install flask 

Set up your OpenAI API key:
On Linux export OPENAI_API_KEY='your-openai-api-key'  
On Windows use `set OPENAI_API_KEY='your-openai-api-key'`

Usage
Starting the Flask API
In the first terminal, run the Flask API:
python api/api.py
The API will start and be accessible at http://127.0.0.1:5000.

Running the Explainer Script
In a second terminal, run the explainer script:
python explainer/explainer.py
The script will continuously check for new files to process in the uploads directory.

Using the Client
The client can be used to upload files and check their processing status. The client supports two commands: upload and status.

Uploading a File
python client/client.py upload path_to_your_file.pptx
This command will upload the specified PowerPoint file and return a unique identifier (UID) for the uploaded file.

Checking the Status
python client/client.py status your_uid
This command will check the processing status of the file identified by the provided UID.

Testing
To run the system tests:
pytest test_system.py
The tests will start the Flask API and explainer script, upload a test file, and verify the processing status.

Project Structure

final-exercise-yoaz11/
├── api/
│   └── api.py
├── client/
│   └── client.py
├── explainer/
│   └── explainer.py
├── fetch_explanation.py
├── main.py
├── extract_text.py
└── test_system.py

Contributions are welcome! Please fork the repository and submit a pull request.