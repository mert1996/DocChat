# DocChat

DocChat is a **Streamlit-based Q&A application** that allows users to ask questions based on their uploaded `.docx` documents.  
The system splits the document into chunks, stores these chunks in a **Weaviate** database, and retrieves the most relevant chunks to generate answers using **GPT-4**.

## Features

- Upload your own Word document and ask questions about its content.
- To minimize costs, the system operates in a **single-question, single-answer** mode.
- **Important:** The app does **not have memory**. It treats every question independently and does not remember previous questions or answers.
- Designed for low-cost, fast responses, and minimal resource usage.

## Initial Setup

Follow these steps to set up the project:

1. **Create a Weaviate Account:**  
   Go to [https://console.weaviate.cloud](https://console.weaviate.cloud) and create a free account.  
   Create a new **Sandbox Deployment** (authentication should be disabled or is disabled by default).

2. **Get an OpenAI API Key:**  
   Go to [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys) and generate a new API key.

3. **Clone the Project:**

```bash
git clone https://github.com/mert1996/DocChat.git
```

4. **Set up a Virtual Environment and Install Requirements:**

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
.\venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

5. **Create a `.env` File:**

Create a file named `.env` in the project root directory with the following content:

```env
OPENAI_API_KEY=your-openai-api-key-here
WEAVIATE_URL=https://your-weaviate-instance-url
WEAVIATE_API_KEY=your-weaviate-api-key-here
```

## Running the Application

To launch the app, run:

```bash
streamlit run main.py
```

Then, in the opened Streamlit web app:

1. **Upload a Document:**  
   Use the sidebar to upload a `.docx` file.

2. **Create Schema:**  
   If needed, click the "Create Schema" button to clear the previous Weaviate data and create a fresh class for your document chunks.

3. **Ask Questions:**  
   Use the chat input to type your questions and receive answers based on the uploaded document content.

> **Note:** Uploading a new document will overwrite any previously uploaded documents. Previous data will be deleted.

## Additional Information

- Only `.docx` files are currently supported.
- Future versions may support `.pdf`, `.txt`, and other document formats.
- The application uses **GPT-4** via OpenAI API. Please be aware of your usage limits.
- The app is built with simplicity and extensibility in mind for future improvements.

## Acknowledgements

This project was built to provide a fast, efficient, and low-cost document-based Q&A experience.  
Feel free to contribute, suggest improvements, or fork it for your own projects!
