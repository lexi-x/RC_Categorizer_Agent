# Gemini Agent

This short guide explains, how to run the Gemini agent script in this folder. It uses Windows Powershell commands, but the syntax should be largely the same or similar to Mac and Linux. 

## Overview

The project contains a Python script that connects to Google Gemini via API. The script needs a secret API key to work. Instead of typing the key into the terminal every time, we recommend keeping it in a small file named `.env` so the program can read it automatically. An example is provided in `.env.example`

Important: keep your API key private. Do not share the `.env` file or upload it to the internet.

## Set Up

1) We recommend downloading VSCode or IntelliJ for a more intuitive code editor to modify the files if necessary, but it can also be done purely on command line. 
    - The program expects a variable called `GOOGLE_API_KEY` in the `.env` file. Make a copy of the `.env.example` and replace it with your actual API key.

2) Create a file named `.env` in the project folder and put your API key inside. 

3) Install the packages outlined in requirements.txt.

    - You can install the packages one-by-one, or install everything listed in `requirements.txt` at once by running this command in terminal:

    ```
    pip install -r requirements.txt
    ```

    - If `pip` is not found, you should download the pip package installer from google and add it to your system environment variables (tutorial on the pip site). Otherwise, you should also be able to install the packages manually from Google.

    - Optionally, you can also initialize a virtual environment to isolate dependencies with
        ```
        python -m venv venv
        .\venv\Scripts\Activate.ps1
        python -m pip install -r requirements.txt
        ```

## Running the Agent

1. Modify the .py file to fit your inputs:
    - Replace `INPUT_FILE` and `OUTPUT_FILE` with the file names of your input and output Excel sheets. If they are not located in the same folder as the agent code, make sure to input the full file path.

2. Specify the desired categories in the `Categories` list. The categories should be as specific and concise as possible, as the agent accuracy decreases when given categories with multiple elements.
    - For example, "marketing/communications" would be a better category than "publicity, outreach, and communication"

3. Change `START_ROW` and `END_ROW` to specify which Excel rows need to be processed. The code assumes zero-indexing, which means the first row of the Excel would be denote "0", and the appropriate offset is added later when writing to the Excel. 
    - For example, if you put 0 to 100, the agent would write to Excel rows 1 through 101.

4. Run the Gemini agent script in terminal using the command

    ```
    python .\ssp_chatbot_gemini.py
    ```
	- The program will add a category column with values in the rows specified above. It is designed to print a message every time one row is done. If you would like to disable this feature, comment out the last line of the program by adding # in front of it. 
    - Before running it, make sure the files being inputted are not open on your desktop, as Python cannot edit actively open files. 

5. IMPORTANT WARNINGS:
    - DO NOT close the program in the middle of running it, as this risks corrupting the entire Excel file if it is in the middle of writing it.
    - If you must terminate the program (Ctrl/Cmd + C) while it is running, make a copy of your excel first to prevent losing data.
    - If using VSCode or IntelliJ, the program will not be affected by turning off/on your computer and will safely pause execution, but you should not hard-terminate in command line.

## Troubleshooting 

- "Cannot access file": the program cannot edit a file that is open on your computer, so make sure to close the files you are reading/writing to before running the program. 

- "Missing module" or "ModuleNotFoundError: No module named 'dotenv'":
  - Run `pip install python-dotenv` again. Make sure you used the same Python installation (`python --version`) you used to run the script.

- "API key missing" or program says the key is not set:
  - Open the `.env` file and confirm it has a line exactly like `GOOGLE_API_KEY=YOUR_KEY_HERE` (no extra spaces or quotes).

- If you run into any other issues, please contact Rice Consulting or directly email me at lx31@rice.edu. Hope this helps!

## Post-processing

The LLM isn't perfect, and Gemini especially has been experiencing inconsistencies recently. After running the agent, I highly recommend scanning the Excel to manually fix entries where the agent gives unusually long responses or non-standard categories. From our experience, this happens about 1% of the time.