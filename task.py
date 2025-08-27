from crewai import Task
from agents import financial_analyst, investment_advisor, risk_assessor, verifier
from tools import FinancialDocumentTool

# Task for the verifier agent to check the document
verification_task = Task(
    description="Verify the provided document located at {file_path}. Check if it is a legitimate financial document. If it is not a financial document, state that clearly.",
    expected_output="A confirmation that the document is a valid financial report, or a statement indicating it is not a valid financial document.",
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool]
)

# Task for the financial analyst agent
financial_analysis_task = Task(
    description="Analyze the financial document located at {file_path}. Provide a detailed summary of the key financial metrics, performance, and overall health of the company. The user's query is: {query}",
    expected_output="A comprehensive report including an executive summary, a detailed analysis of revenue, profit margins, and other key financial indicators. The report should be well-structured and easy to understand.",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool]
)

# Task for the investment advisor agent
investment_analysis_task = Task(
    description="Based on the financial analysis of the document at {file_path}, provide strategic investment recommendations. Consider the user's query: {query}",
    expected_output="A set of clear, actionable investment recommendations. Each recommendation should be justified with data from the financial analysis and a clear assessment of the potential return and risk.",
    agent=investment_advisor,
    tools=[FinancialDocumentTool.read_data_tool]
)

# Task for the risk assessor agent
risk_assessment_task = Task(
    description="Conduct a thorough risk assessment of the company based on the financial document at {file_path}. Identify and evaluate potential market, credit, and operational risks. The user's query is: {query}",
    expected_output="A detailed risk assessment report outlining potential risks, their likelihood, and their potential impact. The report should also suggest mitigation strategies for the identified risks.",
    agent=risk_assessor,
    tools=[FinancialDocumentTool.read_data_tool]
)
