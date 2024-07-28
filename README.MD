# Semantic Chatbot Project
This project implements a semantic chatbot  integrates with various APIs for enhanced functionality.

Features
Natural Language Understanding: Utilizes advanced NLP techniques to interpret and respond to user queries.

Integration with Google APIs: Leverages Google API services for additional functionalities like geolocation and natural language processing.

Persistence: Stores data in a specified directory for maintaining state across sessions.

Model Customization: Allows customization of model parameters and embedding models for specific tasks.

Database Integration: Connects to an SQL database for data storage and retrieval.

Environment Variables
Ensure you have a .env file in the root directory of the project with the following variables:

dotenv
Copy code
# SQL credentials
SQL_IP=

SQL_USER=

SQL_PASSWORD=


# Directory path for persistence
PERSIST_DIRECTORY=

# Project ID
PROJECT_ID=

# Google API key for integration
GOOGLE_API_KEY=

# Google AI credentials path
GOOGLE_AI_CREDENTIALS=

# Model settings
MODEL_TYPE=
MODEL_PATH=
EMBEDDINGS_MODEL_NAME=
MODEL_N_CTX=
MODEL_N_BATCH=
TARGET_SOURCE_CHUNKS=

# Path for static assets
PROMPT_PATH=

# Redis server host
REDIS_HOST=

Copy the above environment variables into .env and replace placeholders with your actual credentials and paths.