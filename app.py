# app.py
# DentiBuddy: A simple Streamlit app for quick dental questions.

# Import necessary libraries
import streamlit as st  # For creating the web app interface
import openai           # To connect with the OpenAI API
import hashlib          # To create a secure hash for session IDs
import os               # To access environment variables for API keys

# --- Configuration ---

# Set up the OpenAI API client
# NOTE: This app is configured to use the free OpenAI GPT-4o-mini model.
# To make this work, you need to set up a Streamlit Secret called "OPENAI_API_KEY".
# 1. Sign up for an OpenAI account and get your API key.
# 2. In your Streamlit Community Cloud account, go to your app's settings.
# 3. Add a new Secret with the key "OPENAI_API_KEY" and paste your key as the value.
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    # This block runs if the secret isn't found, reminding the user to set it.
    st.error("OpenAI API key not found. Please set it in Streamlit Secrets.")
    st.stop() # Stop the app from running further if the key is missing.

# --- Main Application ---

def denti_buddy_app():
    """
    This function runs the main DentiBuddy Streamlit application.
    """

    # --- UI Setup ---

    # Set the title that appears in the browser tab
    st.set_page_config(page_title="DentiBuddy", page_icon="🦷")

    # Display the main title on the page
    st.title("🦷 DentiBuddy")
    st.caption("Your friendly AI dental info assistant")

    # --- Disclaimer ---
    # It's crucial to inform users that this is not a substitute for professional advice.
    st.warning("**Disclaimer:** AI is not a dentist. This tool provides general information only and does not offer medical advice. Consult a qualified dental professional for any health concerns.")

    # --- User Input ---

    # Create a text area for the user to ask their question
    user_question = st.text_area("What's your dental question? (e.g., 'Why do my gums bleed when I floss?')", height=100)

    # Add a slider for the user to indicate their pain level
    pain_level = st.slider("On a scale of 0-10, what is your current pain level?", 0, 10, 0)

    # Create a button to submit the question
    if st.button("Get Answer"):

        # --- Emergency Check ---
        # First, check if the pain level indicates a potential emergency.
        if pain_level >= 6:
            st.error("Pain level 6 or higher can indicate a dental emergency.")
            st.info("Please contact a dental professional immediately.")
            # Provide a button that acts as a link to call a clinic (works on mobile)
            st.link_button("☎️ Call a Local Clinic Now", "tel:555-555-5555") # Placeholder number
        
        # --- Standard Query Processing ---
        # If it's not an emergency, proceed to get an AI-generated answer.
        elif user_question:
            with st.spinner("DentiBuddy is thinking..."):
                try:
                    # --- OpenAI API Call ---
                    # Construct the prompt for the AI model
                    prompt = f"""
                    You are DentiBuddy, an AI assistant providing simple dental information.
                    A user has asked the following question: "{user_question}"
                    Provide a helpful, plain-English answer.
                    IMPORTANT RULES:
                    1. The answer must be 120 characters or less.
                    2. Do not provide medical advice.
                    3. Keep the tone friendly and reassuring.
                    4. Start the answer directly, without any preamble like "Here's your answer:".
                    """

                    # Make the call to the OpenAI API
                    chat_completion = openai.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                        model="gpt-4o-mini", # Using the specified free-tier model
                    )
                    
                    # Extract the answer from the response
                    ai_answer = chat_completion.choices[0].message.content

                    # --- Display Results ---
                    st.subheader("💡 DentiBuddy's Answer")
                    st.write(ai_answer)

                    # Display a fun, related GIF
                    st.markdown("---")
                    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2d0ZzVnaXg4aG15c3B5c2V5c2Z0N3BqZzZzNmY4N3V0aWJtb2NqZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKSjRrfIPjeiVyE/giphy.gif",
                              caption="A little dental humor!", width=200)

                except Exception as e:
                    # Handle potential errors from the API call
                    st.error(f"Sorry, something went wrong. Error: {e}")

            # --- Privacy Information ---
            # Explain how user privacy is maintained.
            st.info("Your privacy is important. No personal information is stored. Your session is identified only by the secure hash below.")
            
            # Create and display a hashed session ID from the user's question.
            # This ensures anonymity as the original question isn't stored or logged.
            session_hash = hashlib.sha256(user_question.encode()).hexdigest()
            st.code(f"Session ID: {session_hash}", language=None)
        else:
            # If the user clicks the button without asking a question
            st.warning("Please enter a question first!")

# --- Run the App ---
# This line makes the app run when the script is executed.
if __name__ == "__main__":
    denti_buddy_app()
