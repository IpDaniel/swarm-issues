# Setup Instructions

1. Create a virtual environment
   python -m venv venv

2. Activate the virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate

3. Install dependencies
   pip install -U "langgraph-cli[inmem]"

4. Populate the .env file
   # Create a file named ".env" in your project root and add the following lines:
   OPENAI_API_KEY=your-openai-api-key
   LANGCHAIN_API_KEY=your-langchain-api-key
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_PROJECT=my-swarm-project

5. Start LangGraph in development mode
   langgraph dev
