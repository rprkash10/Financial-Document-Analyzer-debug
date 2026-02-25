# task.py

from crewai import Task
from agents import (
    financial_analyst,
    verifier,
    investment_advisor,
    risk_assessor
)

# Task to verify the financial document
verification = Task(
    description="""1. Verify the authenticity of the provided financial document.
    2. Check for any inconsistencies or glaring errors in the data.
    3. Confirm that the document is the correct type for financial analysis based on the user's query: {query}.
    4. Summarize the document's purpose and key sections.""",
    expected_output="A concise summary confirming the document's validity and its main sections. If the document is invalid, state why.",
    agent=verifier,
    async_execution=False
)

# Task to analyze the financial document
analyze_financial_document = Task(
    description="""Using the verified financial document, conduct a thorough financial analysis.
    Your analysis should include:
    1. Key financial ratios (e.g., P/E, Debt-to-Equity).
    2. An assessment of the company's revenue, profitability, and cash flow.
    3. A comparison of the current performance with historical trends.
    4. Identification of key financial strengths and weaknesses.""",
    expected_output="A detailed report with sections for financial ratios, performance analysis, and a summary of strengths and weaknesses.",
    agent=financial_analyst,
    async_execution=False,
    context=[verification]
)

# Task for risk assessment
risk_assessment = Task(
    description="""Based on the financial analysis report, conduct a comprehensive risk assessment.
    Identify and evaluate potential risks, including:
    1. Market risks (e.g., competition, economic downturns).
    2. Credit risks (e.g., debt burden, default risk).
    3. Operational risks (e.g., management issues, supply chain).
    4. Provide a final risk score or category (e.g., Low, Medium, High).""",
    expected_output="A structured risk report detailing each category of risk and a concluding risk assessment summary.",
    agent=risk_assessor,
    async_execution=False,
    context=[analyze_financial_document]
)

# Task for providing investment analysis
investment_analysis = Task(
    description="""Synthesize the financial analysis and risk assessment to provide a final investment recommendation.
    Your recommendation should:
    1. State a clear investment thesis (e.g., Buy, Hold, Sell).
    2. Justify the recommendation based on the data from previous tasks.
    3. Suggest a potential investment strategy (e.g., long-term hold, short-term trade).
    4. Include a disclaimer about financial risks.""",
    expected_output="A clear, well-justified investment recommendation memo, including a thesis, strategy, and disclaimers.",
    agent=investment_advisor,
    async_execution=False,
    context=[analyze_financial_document, risk_assessment]
)