**Automate Finances With Python**

Automate Finances With Python is a Python project that helps automate everyday financial tracking and analysis tasks. Key points include:

Read Bank Statements – Load and process CSV bank statements.

Transaction Categorization – Automatically classify income and expenses.

Summarization & Reporting – Compute totals, generate monthly summaries, and track spending trends.

Data Visualization – Optional graphs and charts to analyze finances visually.

Time-Saving – Automates repetitive finance tasks for efficiency.

Beginner-Friendly – Suitable for beginners to intermediate Python learners applying code to real-world finance.

Easy Setup – Minimal requirements with sample data included to get started quickly.

Project Structure

main.py — Main script for data processing and report generation.

sample_bank_statement.csv — Example data for testing.

requirements.txt — Python dependencies for the project.

Requirements & Installation

Prerequisites:

Python 3.8+

Visual Studio Code (with Python extension)

Git

Installation Steps:

Clone the repository:



Create & activate a virtual environment:

# Create virtual environment
python -m venv venv  

# Activate (Windows PowerShell)
venv\Scripts\Activate.ps1  

# Activate (Linux/Mac)
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Run the project (Streamlit app):

streamlit run main.py

Dependencies
streamlit==1.32.0
pandas==2.2.0
plotly==5.18.0
numpy==1.26.4
