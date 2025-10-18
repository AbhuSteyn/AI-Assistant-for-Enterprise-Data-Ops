# Agentic AI Data Quality Assistant

An intelligent data quality monitoring and remediation system powered by LangChain and OpenAI GPT-4. This system autonomously discovers data quality issues, analyzes them, and executes safe fixes or provides recommendations for manual intervention.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Core Components](#core-components)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Contributing](#contributing)
- [License](#license)

## Overview

This AI-powered data quality assistant helps data teams maintain high data quality by:
- Automatically monitoring databases for quality issues
- Detecting anomalies using machine learning
- Analyzing data completeness and integrity
- Executing safe remediation steps
- Providing detailed recommendations for manual review

### Key Features
- 🤖 Autonomous monitoring and remediation
- 📊 Statistical and ML-based anomaly detection
- 🛡️ Safe execution with validation checks
- 📝 Comprehensive logging and reporting
- 🔄 Async-first architecture
- 🎯 LangChain integration for intelligent decision-making

## Project Structure

```plaintext
agentic-data-ops-assistant/
├── data_ops_agent.py    # Main agent orchestration
├── data_scanner.py      # Data quality scanning and analysis
├── connectors.py        # Database connectivity
├── main.py             # Application entry point
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

### File Descriptions

#### `data_ops_agent.py`
The core agent class that orchestrates the entire system:
- Initializes LangChain agent with GPT-4
- Manages tools for scanning and remediation
- Handles decision-making logic
- Maintains conversation memory
- Coordinates between scanning and fixing operations

#### `data_scanner.py`
Implements data quality scanning and analysis:
- Statistical analysis of data distributions
- Anomaly detection using Isolation Forest
- Null value analysis
- Data completeness checking
- Recommendation generation

#### `connectors.py`
Handles database operations:
- Database connection management
- Safe SQL execution
- Fix validation
- Error handling and logging

#### `main.py`
Application entry point:
- Initializes the agent
- Sets up logging
- Runs the monitoring loop
- Handles top-level error management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/agentic-data-ops-assistant.git
cd agentic-data-ops-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Set up environment variables:
```bash
# Required
export OPENAI_API_KEY='your-key-here'

# Optional - Database configuration
export DB_HOST='your-db-host'
export DB_PORT='5432'
export DB_NAME='your-db-name'
export DB_USER='your-db-user'
export DB_PASSWORD='your-db-password'
```

2. Or create a `.env` file:
```plaintext
OPENAI_API_KEY=your-key-here
DB_HOST=your-db-host
DB_PORT=5432
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
```

## Usage

### Basic Usage

1. Run the system:
```bash
python main.py
```

2. Monitor the logs for detected issues and actions taken.

### Advanced Usage

1. Import the agent in your custom script:
```python
from data_ops_agent import DataOpsAgent

async def custom_monitoring():
    agent = DataOpsAgent(openai_api_key='your-key-here')
    results = await agent.monitor_data_quality()
    print(f"Found {len(results)} issues")
```

2. Customize scanning parameters:
```python
from data_scanner import DataQualityScanner

scanner = DataQualityScanner()
scanner.anomaly_detector.contamination = 0.05  # Adjust sensitivity
```

## Core Components

### Data Ops Agent
The agent uses LangChain's OpenAIFunctionsAgent to:
- Process and analyze data quality issues
- Make decisions about remediation steps
- Maintain conversation context
- Execute tools safely

Example agent interaction:
```python
result = await agent.monitor_data_quality()
print(result)
```

### Data Scanner
Implements multiple scanning strategies:
- Statistical analysis
- Anomaly detection
- Completeness checking

Example scanning:
```python
scanner = DataQualityScanner()
issues = await scanner.scan_database()
```

### Database Connector
Handles database operations safely:
- Validates SQL before execution
- Logs all operations
- Provides rollback capabilities

Example fix execution:
```python
connector = DatabaseConnector()
result = await connector.execute_fix({
    "type": "fill_nulls",
    "table": "users",
    "column": "email"
})
```

## Examples

### Monitoring Data Quality
```python
import asyncio
from data_ops_agent import DataOpsAgent

async def monitor():
    agent = DataOpsAgent(openai_api_key='your-key-here')
    results = await agent.monitor_data_quality()
    
    for result in results:
        print(f"Issue: {result['issue']}")
        print(f"Action: {result['action_taken']}")

asyncio.run(monitor())
```

### Custom Analysis
```python
from data_scanner import DataQualityScanner

scanner = DataQualityScanner()
analysis = await scanner.analyze_column(
    table="transactions",
    column="amount"
)
print(analysis['recommendations'])
```

## Best Practices

1. **Safety First**
   - Always validate SQL fixes before execution
   - Use appropriate contamination values for anomaly detection
   - Keep backups before running automated fixes

2. **Monitoring**
   - Set up proper logging
   - Monitor agent decisions
   - Review automated actions regularly

3. **Configuration**
   - Use environment variables for sensitive data
   - Adjust thresholds based on your data characteristics
   - Start with conservative auto-fix settings

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---
Created by [@AbhuSteyn](https://github.com/AbhuSteyn)
Last Updated: 2025-10-18