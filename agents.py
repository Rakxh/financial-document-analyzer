import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import search_tool, FinancialDocumentTool, InvestmentTool, RiskTool

# Load environment variables from .env file
load_dotenv()

# Initialize the language model
llm = ChatGoogleGenerativeAI(model="gemini-pro", verbose=True, temperature=0.1)

# Create an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide a detailed and accurate analysis of financial documents. Focus on key metrics, trends, and potential red flags. Your analysis should be objective and based purely on the data presented in the document.",
    verbose=True,
    memory=True,
    backstory=(
        "With over 20 years of experience in financial analysis, you have a keen eye for detail and a deep understanding of market dynamics. You are known for your meticulous approach and your ability to distill complex financial data into clear, actionable insights. You are a trusted advisor to major investment firms and your reports are highly regarded for their accuracy and depth."
    ),
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    llm=llm,
    allow_delegation=True
)

# Create a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify the authenticity and format of financial documents. Ensure that the document is a legitimate financial report and not some other type of document. Your verification should be swift and accurate.",
    verbose=True,
    memory=True,
    backstory=(
        "As a former compliance officer, you have extensive experience in document verification. You are an expert at identifying the key characteristics of financial reports and can quickly determine if a document is authentic. Your attention to detail is unmatched, and you are committed to maintaining the integrity of the financial analysis process."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    allow_delegation=False
)

# Create an Investment Advisor agent
investment_advisor = Agent(
    role="Investment Advisor",
    goal="Develop strategic investment advice based on the financial analysis. Your recommendations should be well-researched, balanced, and tailored to a typical investor's risk tolerance. Provide a clear rationale for each recommendation.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified financial planner with a proven track record of helping clients achieve their financial goals. You believe in a long-term, diversified investment strategy. You are skilled at translating financial data into practical investment advice and are committed to providing recommendations that are in the best interests of your clients."
    ),
    tools=[FinancialDocumentTool.read_data_tool, search_tool, InvestmentTool.analyze_investment_tool],
    llm=llm,
    allow_delegation=True
)

# Create a Risk Assessor agent
risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="Identify and evaluate potential risks based on the financial document and market conditions. Your assessment should cover market, credit, and operational risks. Provide a balanced view of the risks, avoiding sensationalism.",
    verbose=True,
    memory=True,
    backstory=(
        "As a seasoned risk management professional, you have a deep understanding of the complexities of financial markets. You are an expert at identifying potential risks and assessing their impact. You are known for your calm, rational approach and your ability to provide a clear-eyed view of the risks involved in any investment."
    ),
    tools=[FinancialDocumentTool.read_data_tool, search_tool, RiskTool.create_risk_assessment_tool],
    llm=llm,
    allow_delegation=False
)
