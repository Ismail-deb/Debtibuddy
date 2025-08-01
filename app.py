
import streamlit as st
import requests
import json
import hashlib
import time
import re
import os
from datetime import datetime
from typing import Dict, Any
# Page configuration
st.set_page_config(
    page_title="DentiBuddy 🦷",
    page_icon="🦷",
    layout="centered",
    initial_sidebar_state="collapsed"
)
# Custom CSS for professional styling
st.markdown("""
<style>
:root {
    --primary-color: #00A3A3; /* Bright Teal */
    --secondary-color: #00C2C2; /* Lighter Teal */
    --background-color: #F0FDF4; /* Very Light Mint Green */
    --text-color: #202124; /* Dark Gray for high contrast */
    --light-text-color: #FFFFFF;
    --warning-bg: #FEF3C7; /* Amber */
    --warning-border: #FBBF24;
    --warning-text: #92400E;
    --danger-bg: #FEE2E2; /* Red */
    --danger-border: #EF4444;
    --danger-text: #991B1B;
}
body {
    background-color: var(--background-color);
    color: var(--text-color);
}
.main-header {
    text-align: center;
    color: var(--primary-color);
    font-size: 2.8rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}
.subtitle {
    text-align: center;
    color: #555;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}
.disclaimer {
    background-color: var(--warning-bg);
    border: 1px solid var(--warning-border);
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    color: var(--warning-text);
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.emergency {
    background-color: var(--danger-bg);
    border: 2px solid var(--danger-border);
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    color: var(--danger-text);
    font-weight: bold;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
    100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}
.response-box {
    background-color: #FFFFFF;
    border-left: 5px solid var(--primary-color);
    padding: 1.5rem;
    margin: 1.5rem 0;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.tips-box {
    background-color: #D1FAE5; /* Light Green */
    border: 1px solid #10B981;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}
.session-info {
    background: #E5E7EB;
    border: 1px solid #D1D5DB;
    border-radius: 5px;
    padding: 0.5rem;
    font-family: monospace;
    font-size: 0.8rem;
}
.stButton > button {
    background-image: linear-gradient(to right, var(--primary-color) 0%, var(--secondary-color) 100%);
    color: var(--light-text-color);
    border: none;
    border-radius: 25px;
    padding: 0.85rem 2rem;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 163, 163, 0.2);
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0, 163, 163, 0.3);
}
</style>
""", unsafe_allow_html=True)
class DentiBuddy:
    """
    DentiBuddy - A privacy-focused dental AI assistant
    """
    
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.model_name = os.getenv("OLLAMA_MODEL", "deepseek-r1:8b")
        self.max_response_length = 250
        self.timeout = 60
        
    def generate_session_id(self) -> str:
        """Generate a cryptographically secure hashed session ID for privacy"""
        timestamp = str(time.time())
        random_component = str(hash(timestamp + str(os.urandom(16))))
        combined = f"{timestamp}_{random_component}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def detect_emergency(self, user_input: str) -> Dict[str, Any]:
        """
        Comprehensive emergency detection for dental pain and urgent situations
        Returns dict with emergency status and detected triggers
        """
        user_input_lower = user_input.lower()
        detected_triggers = []
        
        # Pain level patterns (6/10 and above)
        pain_patterns = [
            r'(\d+)/10',              # X/10 format
            r'(\d+)\s*out\s*of\s*10',  # X out of 10 format
            r'pain\s*level\s*(\d+)',   # pain level X format
            r'(\d+)/10\s*pain',       # X/10 pain format
            r'(\d+)\s*on\s*10',       # X on 10 format
            r'scale\s*of\s*(\d+)',    # scale of X format
        ]
        
        for pattern in pain_patterns:
            matches = re.findall(pattern, user_input_lower)
            for match in matches:
                try:
                    pain_level = int(match)
                    if pain_level >= 6:
                        detected_triggers.append(f"Pain level {pain_level}/10")
                        break
                except (ValueError, TypeError):
                    continue
        
        # Severe pain keywords
        severe_pain_keywords = [
            'severe pain', 'extreme pain', 'unbearable pain', 'excruciating',
            'agony', 'torture', 'killing me', 'worst pain', 'screaming'
        ]
        
        for keyword in severe_pain_keywords:
            if keyword in user_input_lower:
                detected_triggers.append(f"Severe pain indicator: '{keyword}'")
                break
        
        # Emergency situation keywords
        emergency_keywords = [
            'emergency', 'urgent', 'asap', 'right now', 'immediately',
            'can\'t sleep', 'cant sleep', 'couldn\'t sleep', 'couldnt sleep',
            'all night', 'kept me awake', 'no sleep'
        ]
        
        for keyword in emergency_keywords:
            if keyword in user_input_lower:
                detected_triggers.append(f"Emergency keyword: '{keyword}'")
        
        # Swelling and infection indicators
        infection_keywords = [
            'swollen', 'swelling', 'pus', 'abscess', 'infection', 'infected',
            'fever', 'face swollen', 'jaw swollen', 'can\'t open mouth'
        ]
        
        for keyword in infection_keywords:
            if keyword in user_input_lower:
                detected_triggers.append(f"Infection indicator: '{keyword}'")
        
        # Trauma keywords
        trauma_keywords = [
            'knocked out', 'broken tooth', 'cracked tooth', 'chipped tooth',
            'accident', 'hit in mouth', 'trauma', 'bleeding', 'blood'
        ]
        
        for keyword in trauma_keywords:
            if keyword in user_input_lower:
                detected_triggers.append(f"Trauma indicator: '{keyword}'")
        
        is_emergency = len(detected_triggers) > 0
        
        return {
            'is_emergency': is_emergency,
            'triggers': list(set(detected_triggers)), # Use set to remove duplicates
            'severity': 'HIGH' if len(detected_triggers) >= 2 else 'MODERATE' if detected_triggers else 'LOW'
        }
    
    def query_ollama(self, prompt: str) -> Dict[str, Any]:
        """
        Query Ollama with comprehensive error handling and response processing
        """
        try:
            start_time = time.time()
            # Enhanced dental prompt for better responses
            dental_prompt = f"""You are DentiBuddy, a knowledgeable dental health assistant. 
            Provide helpful, accurate dental guidance.
            Be professional yet friendly. If serious, recommend seeing a dentist immediately.
            Focus on practical advice and reassurance when appropriate.
            
            Question: {prompt}
            
            Response:"""
            
            payload = {
                "model": self.model_name,
                "prompt": dental_prompt,
                "stream": True,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 128,
                    "stop": ["Question:"]
                }
            }
            
            response = requests.post(
                self.ollama_url, 
                json=payload, 
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'},
                stream=True
            )
            
            response.raise_for_status() 
            answer_parts = []
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        answer_parts.append(chunk.get('response', ''))
                        if chunk.get('done'):
                            break
                    except json.JSONDecodeError:
                        continue
            
            answer = "".join(answer_parts).strip()
            answer = self._clean_response(answer)
            
            if len(answer) > self.max_response_length:
                answer = answer[:self.max_response_length]
                answer = answer.rsplit(' ', 1)[0] + "..."
            
            end_time = time.time()
            return {
                'success': True,
                'response': answer,
                'model_used': self.model_name,
                'response_time': end_time - start_time
            }
                
        except requests.exceptions.HTTPError as e:
             if e.response.status_code == 404:
                return {
                    'success': False,
                    'error': f"Model '{self.model_name}' not found. Try: ollama pull {self.model_name}",
                    'error_type': 'model_not_found'
                }
             else:
                return {
                    'success': False,
                    'error': f"Ollama server error (HTTP {e.response.status_code}): {e.response.text}",
                    'error_type': 'server_error'
                }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': "Cannot connect to Ollama. Make sure it's running: 'ollama serve'",
                'error_type': 'connection_error'
            }
        
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': f"Request timed out after {self.timeout} seconds. The model may be too slow. Try again.",
                'error_type': 'timeout_error'
            }
        
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Network error: {str(e)[:50]}...",
                'error_type': 'network_error'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error while processing response: {str(e)[:50]}...",
                'error_type': 'unknown_error'
            }
    
    def _clean_response(self, response: str) -> str:
        """Clean and format the AI response"""
        prefixes_to_remove = [
            'DentiBuddy says:', 'Answer:', 'Response:', 
            'I recommend:', 'My advice:', 'Suggestion:'
        ]
        
        response = response.strip()
        for prefix in prefixes_to_remove:
            if response.lower().startswith(prefix.lower()):
                response = response[len(prefix):].strip()
        
        response = ' '.join(response.split())
        
        if response and not response.endswith(('.', '!', '?')):
            response += '.'
        
        return response
    
    def get_model_status(self) -> Dict[str, Any]:
        """Check if Ollama and the model are available"""
        try:
            response = requests.get(
                self.ollama_url.replace('/api/generate', '/api/tags'),
                timeout=5
            )
            
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                
                return {
                    'ollama_running': True,
                    'model_available': self.model_name in model_names,
                    'available_models': model_names
                }
            else:
                return {'ollama_running': False, 'model_available': False}
                
        except:
            return {'ollama_running': False, 'model_available': False}
def display_emergency_alert(emergency_info: Dict[str, Any]) -> None:
    """Display emergency alert with specific triggers"""
    severity_icons = {
        'HIGH': '🚨🚨🚨',
        'MODERATE': '🚨',
        'LOW': '⚠️'
    }
    
    icon = severity_icons.get(emergency_info['severity'], '🚨')
    
    st.markdown(f"""
    <div class="emergency">
        {icon} <strong>EMERGENCY DETECTED - {emergency_info['severity']} PRIORITY</strong> {icon}<br><br>
        <strong>Detected Issues:</strong><br>
        {'<br>'.join([f"• {trigger}" for trigger in emergency_info['triggers']])}
        <br><br>
        📞 <strong>IMMEDIATE ACTION REQUIRED:</strong><br>
        • Call your dentist RIGHT NOW<br>
        • If after hours, go to emergency dental clinic<br>
        • If severe swelling/fever, consider ER<br>
        • Don't wait - dental emergencies can be serious!
    </div>
    """, unsafe_allow_html=True)
def display_response(response_data: Dict[str, Any]) -> None:
    """Display AI response with metadata"""
    if response_data['success']:
        st.markdown(f"""
        <div class="response-box">
            <strong>🦷 DentiBuddy says:</strong><br>
            <span style="font-size: 1.1em;">{response_data['response']}</span>
            <br><br>
            <small style="color: #666;">
                Model: {response_data['model_used']} | 
                Response time: {response_data['response_time']:.2f}s
            </small>
        </div>
        """, unsafe_allow_html=True)
    else:
        error_messages = {
            'connection_error': "🔌 Connection Error",
            'model_not_found': "🤖 Model Not Found", 
            'timeout_error': "⏱️ Timeout Error",
            'server_error': "🖥️ Server Error",
            'unknown_error': "❓ Unknown Error"
        }
        
        error_type = response_data.get('error_type', 'unknown_error')
        error_title = error_messages.get(error_type, "❌ Error")
        
        st.error(f"{error_title}: {response_data['error']}")
def main():
    """Main application function"""
    
    if 'dentibuddy' not in st.session_state:
        st.session_state.dentibuddy = DentiBuddy()
        st.session_state.session_id = st.session_state.dentibuddy.generate_session_id()
        st.session_state.query_count = 0
        st.session_state.session_start = datetime.now()
    
    st.markdown('<h1 class="main-header">DentiBuddy 🦷</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI-powered dental health assistant</p>', unsafe_allow_html=True)
    
    status = st.session_state.dentibuddy.get_model_status()
    if not status.get('ollama_running'):
        st.error("🔌 Ollama is not running! Please start it with: `ollama serve`")
        st.stop()
    elif not status.get('model_available'):
        available = status.get('available_models', [])
        st.error(f"🤖 Model '{st.session_state.dentibuddy.model_name}' not found!")
        if available:
            st.info(f"Available models: {', '.join(available)}")
        st.info(f"Install the model with: `ollama pull {st.session_state.dentibuddy.model_name}`")
        st.stop()
    
    st.markdown("""
    <div class="disclaimer">
        <strong>⚠️ IMPORTANT MEDICAL DISCLAIMER</strong><br><br>
        DentiBuddy is an AI assistant for <strong>informational purposes only</strong> and is 
        <strong>NOT a substitute for professional medical advice, diagnosis, or treatment</strong>. 
        <br><br>
        • Always consult a qualified dentist for dental concerns<br>
        • In emergencies, contact your dentist or emergency services immediately<br>
        • Do not delay seeking professional care based on AI responses<br>
        • This tool cannot diagnose conditions or replace clinical examination
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💬 Ask me about your dental concerns:")
    
    user_question = st.text_area(
        "Describe your dental issue or question:",
        placeholder="Example: 'I have sharp pain in my back tooth when I bite down. It started yesterday and keeps getting worse.'",
        height=120,
        key="user_input",
        help="Be specific about your symptoms, when they started, and what makes them better or worse."
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        ask_button = st.button("🦷 Ask DentiBuddy", type="primary", use_container_width=True)
    
    if ask_button and user_question.strip():
        st.session_state.query_count += 1
        
        with st.spinner("🧠 Analyzing your dental question..."):
            emergency_info = st.session_state.dentibuddy.detect_emergency(user_question)
            
            if emergency_info['is_emergency']:
                display_emergency_alert(emergency_info)
            
            response_data = st.session_state.dentibuddy.query_ollama(user_question)
            display_response(response_data)
            
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.image(
                    "https://media.giphy.com/media/3o7btNa0RUYa5E7iiQ/giphy.gif", 
                    caption="Keep that smile healthy! 😊", 
                    width=200
                )
    
    elif ask_button and not user_question.strip():
        st.warning("Please describe your dental concern before asking!")
    
    with st.sidebar:
        st.markdown("### 🦷 Essential Dental Care")
        st.markdown("""
        <div class="tips-box">
        <strong>Daily Routine:</strong><br>
        • Brush 2x daily with fluoride toothpaste<br>
        • Floss daily to remove plaque<br>
        • Use mouthwash for extra protection<br>
        • Replace toothbrush every 3 months<br><br>
        
        <strong>Healthy Habits:</strong><br>
        • Limit sugary and acidic foods<br>
        • Don't use teeth as tools<br>
        • Wear mouthguard for sports<br>
        • Stay hydrated with water
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🚨 See a Dentist IMMEDIATELY if:")
        st.markdown("""
        - **Severe, persistent pain**
        - **Facial or gum swelling**
        - **Knocked out or broken tooth**
        - **Uncontrolled bleeding**
        - **Signs of infection (fever, pus)**
        - **Difficulty swallowing/breathing**
        """)
        
        st.markdown("### 📊 Session Info")
        session_duration = datetime.now() - st.session_state.session_start
        st.markdown(f"""
        <div class="session-info">
        <strong>Session:</strong> {st.session_state.session_id}<br>
        <strong>Queries:</strong> {st.session_state.query_count}<br>
        <strong>Duration:</strong> {str(session_duration).split('.')[0]}<br>
        <strong>Model:</strong> {st.session_state.dentibuddy.model_name}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("*🔒 Your privacy is protected - no personal data stored*")
        
        st.markdown("### 🔧 Quick Actions")
        if st.button("🔄 New Session", help="Start fresh with new session ID"):
            for key in ['dentibuddy', 'session_id', 'query_count', 'session_start', 'user_input']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        if st.button("🧹 Clear Input", help="Clear the question box"):
            st.session_state.user_input = ""
            st.rerun()
if __name__ == "__main__":
    main()
