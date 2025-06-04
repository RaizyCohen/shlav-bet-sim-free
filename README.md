# Internal Medicine Oral Exam Simulator

This is a Streamlit-based application that simulates internal medicine oral exams for Israeli 'Shlav Bet' residency training.

## Setup Instructions

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv_new
   source venv_new/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API Key:**
   You need to set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="your_actual_api_key_here"
   ```
   
   Or create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

4. **Run the application:**
   ```bash
   streamlit run "shlav bet 2.py"
   ```

## Features

- Personalized case generation based on residency year and experience
- Interactive patient simulation
- Performance evaluation and analytics
- Adaptive difficulty based on performance

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for API calls 