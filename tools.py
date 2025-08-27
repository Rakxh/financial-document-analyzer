import os
from dotenv import load_dotenv
from crewai_tools import PDFSearchTool, SerperDevTool

# Load environment variables from .env file
load_dotenv()

# Creating search tool
search_tool = SerperDevTool()

# Creating custom pdf reader tool
class FinancialDocumentTool:
    @staticmethod
    def read_data_tool(path: str = 'data/sample.pdf') -> str:
        """
        Tool to read data from a pdf file from a path.

        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Financial Document file content.
        """
        # Instantiate the PDFSearchTool with the provided file path
        pdf_tool = PDFSearchTool(pdf=path)
        # The 'run' method of PDFSearchTool reads the document
        docs = pdf_tool.run()
        
        # The tool returns the content as a single string, so we can return it directly.
        return docs

# Creating Investment Analysis Tool
class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data: str) -> str:
        """
        Analyzes financial document data for investment insights.
        NOTE: This is a placeholder and does not perform real analysis.
        """
        # In a real-world scenario, you would implement your analysis logic here.
        # For this exercise, we'll return a placeholder string.
        return "Investment analysis based on the document suggests a balanced portfolio approach. Further market research is recommended."

# Creating Risk Assessment Tool
class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data: str) -> str:
        """
        Creates a risk assessment based on financial document data.
        NOTE: This is a placeholder and does not perform real risk assessment.
        """
        # In a real-world scenario, you would implement your risk assessment logic here.
        # For this exercise, we'll return a placeholder string.
        return "Risk assessment indicates moderate market risk. Diversification is advised to mitigate potential downturns."
