# Setup Instructions

1. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**
   ```bash
   pip install -U "langgraph-cli[inmem]"
   ```

4. **Start LangGraph in development mode**
   ```bash
   langgraph dev
   ```
