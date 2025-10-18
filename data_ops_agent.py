from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.tools import Tool
from typing import List, Dict
import logging
from datetime import datetime

from .data_scanner import DataQualityScanner
from .connectors import DatabaseConnector

class DataOpsAgent:
    """
    Main agent class that orchestrates data quality monitoring and remediation
    using LangChain's capabilities
    """
    
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4",
            openai_api_key=openai_api_key
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.scanner = DataQualityScanner()
        self.connector = DatabaseConnector()
        
        self.agent_executor = self._initialize_agent()
    
    def _initialize_agent(self) -> AgentExecutor:
        """Initialize the LangChain agent with tools and system prompt"""
        tools = [
            Tool(
                name="scan_data_quality",
                func=self.scanner.scan_database,
                description="Scan database tables for data quality issues"
            ),
            Tool(
                name="analyze_column",
                func=self.scanner.analyze_column,
                description="Analyze a specific column for anomalies and quality issues"
            ),
            Tool(
                name="fix_data_issue",
                func=self.connector.execute_fix,
                description="Execute a SQL fix for a data quality issue"
            )
        ]
        
        system_prompt = SystemMessage(content="""
        You are an AI Data Quality Assistant that helps identify and fix data issues.
        When you find issues:
        1. Analyze the severity and impact
        2. Propose safe fixes that won't corrupt data
        3. Execute fixes only when confident, otherwise recommend manual review
        Always log your actions and reasoning.
        """)
        
        prompt = OpenAIFunctionsAgent.create_prompt(
            system_message=system_prompt,
            extra_prompt_messages=[MessagesPlaceholder(variable_name="chat_history")]
        )
        
        agent = OpenAIFunctionsAgent(
            llm=self.llm,
            tools=tools,
            prompt=prompt
        )
        
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            memory=self.memory,
            verbose=True,
            max_iterations=3
        )
    
    async def monitor_data_quality(self) -> List[Dict]:
        """Main method to monitor and fix data quality issues"""
        try:
            # Scan for issues
            issues = await self.scanner.scan_database()
            if not issues:
                return []
            
            results = []
            for issue in issues:
                # Let the agent analyze and handle each issue
                result = await self.agent_executor.arun(
                    input=f"Analyze and handle this data quality issue: {issue}"
                )
                
                results.append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "issue": issue,
                    "action_taken": result
                })
                
            return results
            
        except Exception as e:
            logging.error(f"Error in data quality monitoring: {str(e)}")
            raise