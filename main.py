import asyncio
import logging
from datetime import datetime
import os
from data_ops_agent import DataOpsAgent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    # Initialize the agent
    agent = DataOpsAgent(
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )
    
    try:
        logging.info("Starting data quality monitoring...")
        results = await agent.monitor_data_quality()
        
        if results:
            logging.info(f"Found and processed {len(results)} issues:")
            for result in results:
                logging.info(f"Issue: {result['issue']}")
                logging.info(f"Action: {result['action_taken']}")
        else:
            logging.info("No data quality issues found")
            
    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())