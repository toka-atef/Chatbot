
# Chatbot System

This project is designed to create a chatbot that interacts with purchase order data stored in MongoDB. It uses NLP embeddings and vector search to enable efficient and accurate data retrieval. Before you start, ensure that you set up the environment variables correctly.

## Prerequisites

- Python 3.8 or later
- MongoDB database with the required data
- A MongoDB connection URL for your database

## Setup Instructions

1. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```
2. ** Download Example Dataset:**

   -You can download the example dataset from this[Link](https://www.kaggle.com/datasets/sohier/large-purchases-by-the-state-of-ca/)
   

3. **Configure Environment Variables:**
   - Update the following variables to the `.env` file:

   - Replace `<your_mongodb_connection_url>` with the connection string to your MongoDB database.
   - Replace `<your_database_name>` with the name of your database.

4. **Initial Data Upload and Embedding Creation** (only for first-time setup):
   - If this is your first time running the application, you'll need to upload data to the MongoDB database and create embeddings.
   - Run the following scripts in order:

     ```bash
     python mongo_upload_data.py
     python mongo_create_embedding.py
     ```

   - **Note:** If you have already uploaded the data to the database, you can skip these steps.

5. **Run the Chatbot:**
   ```bash
   streamlit run app.py
   ```

## Usage

After starting the application, a Streamlit interface will open where you can enter queries and interact with the chatbot. The chatbot will use the data in your MongoDB database to answer questions based on the purchase order information.
