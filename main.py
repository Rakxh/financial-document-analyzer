from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
from crewai import Crew, Process
from agents import financial_analyst, investment_advisor, risk_assessor, verifier
from task import financial_analysis_task, investment_analysis_task, risk_assessment_task, verification_task
import asyncio

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str):
    """To run the whole crew"""
    
    # The verifier agent's task needs to be run first to ensure the document is valid.
    verification_crew = Crew(
        agents=[verifier],
        tasks=[verification_task],
        process=Process.sequential,
        verbose=2
    )
    
    # The input for the verification task is the file_path.
    verification_result = verification_crew.kickoff(inputs={'file_path': file_path})
    
    # If the document is not a valid financial document, we should stop the process.
    if "not a valid financial document" in verification_result.lower():
        raise HTTPException(status_code=400, detail=f"The provided document is not a valid financial document. Verification result: {verification_result}")

    # If the document is valid, we can proceed with the other agents.
    financial_crew = Crew(
        agents=[financial_analyst, investment_advisor, risk_assessor],
        tasks=[financial_analysis_task, investment_analysis_task, risk_assessment_task],
        process=Process.sequential,
        verbose=2
    )
    
    # The input for the financial crew includes both the query and the file path.
    result = financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_financial_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights, risks, and a general overview.")
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        if not query:
            query = "Analyze this financial document for investment insights, risks, and a general overview."
        
        # Since run_crew is a synchronous function, we run it in a separate thread
        # to avoid blocking the FastAPI event loop.
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, run_crew, query.strip(), file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except HTTPException as e:
        # Re-raise HTTPException to let FastAPI handle it.
        raise e
    except Exception as e:
        # For any other exceptions, return a 500 internal server error.
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                # Log the error if you have a logging setup.
                print(f"Error removing file {file_path}: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
