DentiBuddy 🦷

DentiBuddy is a minimal, privacy-focused Python web application built with Streamlit. It uses OpenAI's GPT-4o-mini model to provide simple, plain-English answers (≤ 120 characters) to common dental questions.

 Features

-   **AI-Powered Answers:** Leverages the free-tier GPT-4o-mini model for quick dental information.
-   **Emergency Flagging:** Identifies user-reported pain levels of 6/10 or higher and prompts them to call a dental clinic immediately.
-   **Privacy First:** Does not store any Personal Identifiable Information (PII). Each query is anonymized with a hashed session ID.
-   **User-Friendly:** Includes a simple interface and a fun cartoon GIF with each answer.
-   **Important Disclaimer:** Clearly states that the tool is not a substitute for professional medical advice.

 How to Run Locally

Follow these steps to run DentiBuddy on your own computer.

 1. Prerequisites

-   Python 3.8 or newer installed.
-   An API key from OpenAI.

 2. Setup

1.  **Clone the repository or download the files (`app.py`, `requirements.txt`).**

2.  **Create and activate a virtual environment:**
    -   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    -   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  Set up your OpenAI API Key:**
    -   Create a folder named `.streamlit` in your project directory.
    -   Inside it, create a file named `secrets.toml`.
    -   Add your OpenAI API key to this file like so:
        ```toml
        # .streamlit/secrets.toml
        OPENAI_API_KEY="your-api-key-goes-here"
        ```

 3. Run the App

-   Open your terminal, navigate to the project folder, and run:
    ```bash
    streamlit run app.py
    ```
-   Your web browser will open with the DentiBuddy app running.

 How to Deploy to Streamlit Community Cloud

1.  **Push your code to a public GitHub repository.**
    -   Make sure your repository includes `app.py`, `requirements.txt`, and this `README.md`.
    -   **Do not** commit your `secrets.toml` file. It's best to add `.streamlit/secrets.toml` to a `.gitignore` file.

2.  **Sign up or log in** to [Streamlit Community Cloud](https://share.streamlit.io/).

3.  **Click "New app"** and connect your GitHub account.

4.  **Select your repository and the `app.py` file.**

5.  **Go to the "Advanced settings..." section.**
    -   In the "Secrets" text box, add your OpenAI API key in the same format as the `secrets.toml` file:
        ```toml
        OPENAI_API_KEY="your-api-key-goes-here"
        ```

6.  Click "Deploy! and wait for your app to go live.
