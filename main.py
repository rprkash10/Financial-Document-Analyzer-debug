# main.py

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import traceback
from contextlib import asynccontextmanager

# Import CrewAI components
from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, investment_analysis, risk_assessment, verification

# Import database functions
from database import connect_to_db, save_analysis

# This lifespan manager connects to the DB on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    connect_to_db()
    yield
    print("Application shutdown.")

# Update the FastAPI app instance to use the lifespan manager
app = FastAPI(title="Financial Document Analyzer", lifespan=lifespan)


def run_crew(query: str, file_path: str):
    """To run the whole crew"""
    inputs = {
        'query': query,
        'file_path': file_path
    }

    financial_crew = Crew(
        agents=[
            verifier,
            financial_analyst,
            risk_assessor,
            investment_advisor
        ],
        tasks=[
            verification,
            analyze_financial_document,
            risk_assessment,
            investment_analysis
        ],
        process=Process.sequential,
        verbose=2
    )
    
    result = financial_crew.kickoff(inputs=inputs)
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document, provide recommendations, and save to database"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        if not query:
            query = "Analyze this financial document for investment insights"
            
        # Run the CrewAI analysis
        response = run_crew(query=query.strip(), file_path=file_path)
        
        # Save the successful analysis to the database
        analysis_str = str(response)
        save_analysis(query=query, file_name=file.filename, analysis_result=analysis_str)
        print(f"Successfully saved analysis for {file.filename} to the database.")
        
        return {
            "status": "success",
            "query": query,
            "analysis": analysis_str,
            "file_processed": file.filename
        }
        
    except Exception as e:
        print("--- DETAILED TRACEBACK ---")
        traceback.print_exc()
        print("--------------------------")
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)