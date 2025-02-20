# langchain Gemini Agent

## Project Overview
This project is designed to store GitHub issues in a vector database, enabling users to retrieve relevant issues by querying in natural language. Additionally, users can add notes (note.txt) for reference and save retrieved issues if needed.

Features:
Issue Retrieval: Users can query the system for issues related to a specific topic, leveraging vector search for efficient matching.
Note Management: Users can add personal notes, which are stored in note.txt.
Issue Saving: Retrieved issues can be saved for future reference.
Integration: Utilizes LangChain for AI-driven retrieval, Gemini API for natural language understanding, and Datastax AstraDB as the vector database backend.

### Setup Instructions
1. Install Dependencies


``` python -m venv <name_env>
source <name_env>/bin/activate  # For macOS/Linux
<name_env>\Scripts\activate  # For Windows
pip install -r requirements.txt
 ```

2. Configure Environment Variables
Create a .env file with the following credential

``` 
GITHUB_TOKEN = ""
ASTRA_DB_API_ENDPOINT = ""
ASTRA_DB_APPLICATION_TOKEN = ""
ASTRA_DB_KEYSPACE = ""
GOOGLE_API_KEY = ""
```
3. Run the Agent
```python main.py```


