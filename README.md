# 🤖 Loan Advisor Chatbot – NLP and Machine Learning

An AI-powered Loan Advisor Chatbot built using Python, Natural Language Processing (NLP), and Machine Learning. The application helps users explore loan-related information, check estimated loan eligibility, calculate EMIs, and complete a guided loan application conversation through an interactive Streamlit interface.

## 📌 Project Overview

The Loan Advisor Chatbot understands user queries, identifies their intent, extracts important loan-related information, and guides users through relevant conversational workflows.

It combines NLP-based intent classification, rule-based entity extraction, a Machine Learning loan eligibility prediction model, and an EMI calculator in a single application.

## 🎯 Project Objectives

- Build an interactive chatbot for loan-related assistance.
- Identify user intentions using NLP and Machine Learning.
- Extract important financial details from natural language messages.
- Estimate loan eligibility using a Random Forest classification model.
- Calculate monthly EMI, total interest, and total repayment.
- Collect and validate loan application details through conversational workflows.

## ✨ Key Features

### 1. NLP-Based Intent Classification
- Identifies the intent behind user messages.
- Routes queries to appropriate chatbot responses and workflows.
- Supports different loan-related conversational scenarios.

### 2. Loan Entity Extraction
Uses Regular Expressions (Regex) and rule-based patterns to extract important loan details, including:

- Income
- Income frequency
- Loan amount
- Loan type
- Loan tenure
- Interest rate
- CIBIL score
- Number of dependents
- Existing loans

### 3. Loan Eligibility Prediction
- Uses a Random Forest classification model.
- Processes applicant information and financial attributes.
- Generates an estimated loan eligibility prediction.

### 4. EMI Calculator
Calculates:
- Monthly EMI
- Total interest payable
- Total repayment amount

### 5. Conversational Loan Application
- Collects applicant information step by step.
- Validates user inputs.
- Displays an application summary.
- Supports confirmation and correction of submitted details.

### 6. Interactive Streamlit Interface
- Chat-based user interface.
- Sidebar navigation.
- Loan eligibility and EMI workflows.
- Interactive user experience.

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| NLP | Intent Classification, Text Processing, Regex, Entity Extraction |
| Machine Learning | Random Forest, Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Frontend | Streamlit |
| Model Serialization | Joblib |
| Development Tools | Jupyter Notebook, VS Code, Git, GitHub |

## 🏗️ Project Architecture

The application follows a modular architecture:

1. **User Input:** User enters a loan-related query through the Streamlit chatbot.
2. **Intent Classification:** The NLP component identifies the user's intent.
3. **Entity Extraction:** Relevant loan information is extracted from the message.
4. **Conversation Management:** The conversation manager controls the workflow and handles user responses.
5. **Loan Prediction:** The Machine Learning model estimates loan eligibility when applicant information is available.
6. **EMI Calculation:** The EMI calculator calculates repayment details when requested.
7. **Chatbot Response:** The application displays the appropriate response through Streamlit.

## 🔄 Application Workflow

```text
User Input
    |
    v
Intent Classification
    |
    v
Entity Extraction
    |
    v
Conversation Manager
    |
    +----------------------+
    |          |           |
    v          v           v
Loan         EMI         Loan
Eligibility  Calculator  Information
Prediction
    |          |           |
    +----------+-----------+
               |
               v
        Chatbot Response
               |
               v
        Streamlit Interface
```

## 📂 Project Structure

```text
```text
LOAN_ADVISOR_CHATBOT/
│
├── app/
│   └── app.py
│
├── Data/
│   ├── processed/
│   │   └── loan_intents_cleaned.csv
│   │
│   └── raw/
│       ├── loan_approval_dataset.csv
│       └── loan_intents.csv
│
├── models/
│   ├── intent_classifier.pkl
│   ├── intent_tfidf.pkl
│   ├── loan_approval_features.pkl
│   ├── loan_approval_rf.pkl
│   ├── lr_tfidf_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── notebooks/
│   ├── 01_intent_eda.ipynb
│   ├── 02_intent_preprocessing.ipynb
│   ├── 03_intent_classification.ipynb
│   ├── 04_entity_extraction.ipynb
│   └── 05_loan_approval.ipynb
│
├── src/
│   ├── bot_engine.py
│   ├── conversation_manager.py
│   ├── emi_calculator.py
│   ├── entity_extraction.py
│   ├── input_validation.py
│   ├── debug_dependents.py
│   ├── debug_emi_workflow.py
│   ├── intrest_test.py
│   ├── main.py
│   ├── requirements.txt
│   ├── test_advanced_extraction.py
│   ├── test_all_entities.py
│   ├── test_chatbot_improvements.py
│   ├── test_conversation_recovery.py
│   ├── test_emi_integration.py
│   ├── test_emi.py
│   ├── test_end_to_end.py
│   ├── test_entity_extraction.py
│   ├── test_entity_mapping.py
│   └── test_entity_validation.py
│
├── .gitignore
└── README.md
```

```
```

*The structure above is illustrative. Update it to match the files actually included in your repository.*

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version
- pip package manager
- GitHub repository

### Step 1: Clone the Repository

```bash
git clone https://github.com/sourabh1432/Loan-Advisor-Chatbot.git
```

### Step 2: Navigate to the Project Directory

```bash
cd Loan-Advisor-Chatbot
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Streamlit Application

```bash
python -m streamlit run app/app.py
```

The application will open in your browser.

## 🧪 Testing and Validation

The project includes testing of important chatbot workflows, including:

- Intent classification and query routing.
- Loan entity extraction.
- Input validation.
- EMI calculation.
- Loan application data collection.
- Application summary, confirmation, and correction.
- Conversation reset and workflow switching.


## 🚀 Future Enhancements

- Improve intent classification using larger and more diverse training datasets.
- Enhance entity extraction to handle more natural language variations.
- Integrate a real-time financial information source.
- Add database integration for secure application data management.
- Improve model evaluation using representative real-world datasets.
- Deploy the application to a cloud platform.

## ⚠️ Disclaimer

This project is developed for educational and demonstration purposes. Loan eligibility predictions are estimates generated by a Machine Learning model and do not represent actual approval by a bank or financial institution. EMI calculations are illustrative and may differ from actual lender offers.

Do not enter real sensitive financial or personal information into a publicly accessible demonstration.

## 👨‍💻 Developer

**Sourabh Patil**

- **GitHub:** https://github.com/sourabh1432
- **LinkedIn:** https://www.linkedin.com/in/sourabh-patil-ab01433a0/
- **Email:** patilsourabh1432@gmail.com

---

⭐ If you find this project useful, consider giving the repository a star!
