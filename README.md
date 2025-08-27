Financial Document Analyzer - Debug Assignment (Fixed)
Project Overview
A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents. This version of the project has been debugged and refactored for proper functionality.

Getting Started
Prerequisites
Python 3.8+

A Google API Key with the Gemini API enabled.

Setup and Usage Instructions
Clone the repository:

git clone <your-repo-link>
cd <your-repo-name>

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the required libraries:

pip install -r requirements.txt

Create a .env file in the root of the project and add your Google API Key:

GOOGLE_API_KEY="YOUR_API_KEY"
SERPER_API_KEY="YOUR_SERPER_KEY"

Run the application:

uvicorn main:app --reload

The application will be running at http://127.0.0.1:8000.

API Documentation
Analyze a Financial Document
Endpoint: /analyze

Method: POST

Description: Uploads a financial document (PDF) and an optional query to receive a detailed analysis.

Request Body: multipart/form-data

file: The PDF file to be analyzed. (Required)

query: A string with your specific question about the document. (Optional)

Success Response:

Code: 200 OK

Content:

{
  "status": "success",
  "query": "Analyze this financial document for investment insights, risks, and a general overview.",
  "analysis": "...",
  "file_processed": "TSLA-Q2-2025-Update.pdf"
}

Error Response:

Code: 400 Bad Request (if the document is not a valid financial document)

Code: 500 Internal Server Error (for other processing errors)

Bugs Found and Fixes
Here's a summary of the bugs I found and how I fixed them:

1. main.py
Bug: The run_crew function was synchronous but called from an async function without await, which would block the server. Also, the crew was not structured correctly.

Fix: I wrapped the call to run_crew in asyncio.get_event_loop().run_in_executor() to run it in a separate thread. I also restructured the crew to first run a verification_crew to validate the document before proceeding with the main financial_crew.

2. agents.py
Bug: The llm = llm line was causing a NameError. The agent prompts were satirical and not useful.

Fix: I replaced llm = llm with a proper instantiation of the ChatGoogleGenerativeAI model. I rewrote the prompts for all agents to be professional and goal-oriented.

3. task.py
Bug: The task descriptions were not serious and would have produced poor results. The tasks were also not well-defined.

Fix: I rewrote all the task descriptions and expected outputs to be clear, professional, and aligned with the goals of the agents. I also created a new verification_task.

4. tools.py
Bug: The FinancialDocumentTool was using an undefined Pdf class and was an async function, which is incompatible with CrewAI tools.

Fix: I replaced the incorrect implementation with the PDFSearchTool from crewai_tools and made the method a static, synchronous function. I also made the other tool methods static for consistency.

5. requirements.txt
Bug: The file was missing essential packages like python-dotenv, langchain-google-genai, and uvicorn. The crewai version was also a bit outdated.

Fix: I added the missing dependencies and updated the versions to ensure compatibility.

I've also included the TSLA-Q2-2025-Update.pdf file you provided so you can test the application right away. Let me know if you have any other questions!