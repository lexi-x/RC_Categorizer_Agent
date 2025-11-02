import os
from dotenv import load_dotenv
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import openpyxl


INPUT_FILE = "input_file.xlsx" 
OUTPUT_FILE = "output_file.xlsx"  

CATEGORIES = ["Strategy Consulting", "Engineering Consulting",
              "Architectural Consulting", "Environmental Consulting", "IT & Software",
              "Legal Services", "Individual Suppliers/Contractors",
              "Marketing, Events, and Communications", "HR & Staffing",
              "Facilities & Operations", "Training",
              "Financial Services", "Educational Suppliers", "Health Insurance, Programs, and Benefits", 
              "Risk/Property Insurance", "Research Contributions"]

# Load .env file if python-dotenv is available. 
# If not available, the code will read the value from the environment.
if load_dotenv is not None:
    load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Google Gemini Flash LLM initialization
if not GOOGLE_API_KEY:
    raise RuntimeError(
        "Google API key not found. Please create a `.env` file with `GOOGLE_API_KEY=...` "
        "or set the environment variable in your terminal. To install python-dotenv: `pip install python-dotenv`."
    )

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=GOOGLE_API_KEY,
)

prompt = PromptTemplate(
    input_variables=["name", "description", "categories"],
    template="""
    You are an expert business analyst.
    Categorize the following company name and description into ONE of the categories below.
    Be as specific as possible, and do not use One-Time Individual Suppliers/Contractors unless absolutely necessary.
    If an input is too long, only analyze the first 50 words.

    Categories: {categories}

    Company Name:
    {name}

    Company Description:
    {description}

    Respond ONLY with the category name.
    """
)

chain = prompt | llm

# Read data from Excel
df = pd.read_excel(INPUT_FILE)

# Ensure required columns exist
if not {"Company Name", "Description"}.issubset(df.columns):
    raise ValueError("Input file must contain 'Company Name' and 'Description' columns")

# Specify start and end rows here
START_ROW = 0
END_ROW = 3800

wb = openpyxl.load_workbook(OUTPUT_FILE)
ws = wb.active

for i in range(START_ROW, END_ROW): 
    name = str(df.iloc[i]["Company Name"])
    description = str(df.iloc[i]["Description"])
    
    response = chain.invoke({
        "name": name, 
        "description": description,
        "categories": ", ".join(CATEGORIES)
    })
    
    category = response.content.strip()

    # Offset to fit excel indices
    ws.cell(i + 2, 4).value = category  
    wb.save(OUTPUT_FILE)
    print(f"Done {i}")
