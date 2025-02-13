# Mock-Interview

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
The **Mock-Interview** application is an interactive Streamlit-based chatbot designed to simulate job interviews. Users provide their background details, including name, experience, and skills, and the chatbot dynamically generates interview questions based on the selected role and company. The chatbot conducts the interview and provides feedback with a score at the end.

## Features
- Interactive chatbot that simulates HR interviews
- Customizable interview setup based on user input
- Supports multiple job levels and positions
- AI-generated interview responses using OpenAI's API
- Feedback generation with an overall score
- Simple and user-friendly Streamlit UI

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/Iblouse/Mock-Interview.git
   cd Mock-Interview
   ```

2. Create a virtual environment:
   ```sh
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows:**
     ```sh
     venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```sh
     source venv/bin/activate
     ```

4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   - Create a `.streamlit/secrets.toml` file and add your OpenAI API key:
     ```toml
     [secrets]
     OPENAI_API_KEY = "your-api-key-here"
     ```

6. Run the application:
   ```sh
   streamlit run app.py
   ```

## Project Structure
```
Mock-Interview/
│-- .gitignore           # Git ignore file
│-- .streamlit/          # Streamlit configuration directory
│   └── secrets.toml     # Secrets file for storing API keys
│-- app.py               # Main application script
│-- requirements.txt     # Project dependencies
│-- README.md            # Project documentation
```

## Usage
1. Run the application using Streamlit.
2. Enter your personal details, experience, and skills.
3. Choose the job level, position, and company.
4. Click "Start Interview" to begin the session.
5. Respond to chatbot questions.
6. Receive feedback at the end of the interview.

## Dependencies
- `streamlit`
- `openai`
- `streamlit_js_eval`

To install all dependencies, run:
```sh
pip install -r requirements.txt
```

## Contributing
Contributions are welcome! Feel free to submit issues and pull requests to improve this project.

## License
This project is licensed under the MIT License.

