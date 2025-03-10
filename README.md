
# JD/CV Matching System

[![Streamlit](https://img.shields.io/badge/Streamlit-App-brightgreen)](https://jdcvmatching-jbcmtsfkcuw6p5tw69pqzn.streamlit.app/)

The JD/CV Matching System is an AI-powered application that analyzes job descriptions (JD) and candidate resumes (CV) to rank candidates based on how well their skills match the requirements specified in the JD. The system uses natural language processing (NLP) techniques for skill extraction (using a curated skills dictionary from LinkedIn skills), experience extraction, and email extraction, while combining cosine similarity and weighted skill importance for ranking.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture & Workflow](#architecture--workflow)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Project Access](#project-access)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

The JD/CV Matching System is designed to help recruiters and hiring managers efficiently screen resumes. By extracting key skills from a job description using a complete list of LinkedIn skills (stored in a `skills.json` file), the system compares these requirements against candidate CVs and ranks them based on:
- **Cosine Similarity:** A measure of textual similarity between the JD and CV using sentence embeddings.
- **Skill Importance:** A normalized score based on the frequency of required skills in the JD that are also present in the candidate’s CV.
- **Email Extraction:** For easier candidate communication, each CV also has an email extracted and displayed.

The final ranking is presented via an intuitive Streamlit dashboard.

## Features

- **Skill Extraction:**  
  Uses a curated `skills.json` file containing a comprehensive list of LinkedIn skills. Only skills that exactly match (using regex word boundaries) in the JD and CV are considered.
  
- **Experience Extraction:**  
  Extracts phrases indicating years of experience using regex patterns to capture details such as "3 years", "5+ years in ..." etc.
  
- **Email Extraction:**  
  Detects and extracts the candidate's email address from their resume text.
  
- **Text Similarity Ranking:**  
  Computes cosine similarity between job description and resume texts using Sentence Transformers.
  
- **Skill Importance Ranking:**  
  Uses the frequency of required skills in the JD as a weighting factor. The final ranking score is a weighted average of the cosine similarity and the normalized skill importance.
  
- **User Interface:**  
  A clean, interactive Streamlit dashboard for file uploads, ranking display, and detailed candidate view.

## Architecture & Workflow

The project is organized into several modules:

- **main.py:**  
  Handles the Streamlit user interface for uploading the JD and CV files, processing them, and displaying the ranking results.

- **processing/parser.py:**  
  Provides methods to extract text from PDF and DOCX files using PyPDF2 and python-docx.

- **processing/processor.py:**  
  Uses spaCy, KeyBERT, and Sentence Transformers to extract skills, experience, and emails from the text. It loads a skills list from `skills.json` for precise skill matching.

- **processing/matching.py:**  
  Ranks candidates by computing:
  - Cosine similarity between the JD and CV embeddings.
  - A normalized skill importance percentage based on the frequency of JD skills.
  - The final score as a weighted average of the two metrics.

- **processing/skills.json:**  
  A JSON file containing a curated list of LinkedIn skills. This file is used by the processor to match and extract skills from the input texts.

### Workflow Diagram

1. **Job Description Processing:**  
   - Upload JD file → Extract text via `parser.py` → Process text with `processor.py` to extract skills, experience, and email → Generate embedding.

2. **Resume Processing:**  
   - Upload CV files → Extract text via `parser.py` → Process text with `processor.py` to extract skills, experience, and email → Generate embedding.

3. **Candidate Ranking:**  
   - Compare JD skills with each CV's extracted skills → Compute cosine similarity → Calculate skill importance scores → Combine into final ranking score using `matching.py`.

4. **Dashboard Display:**  
   - Display candidate rankings (name, final score, email) and detailed candidate information on the Streamlit dashboard.

## Installation & Setup

### Prerequisites

- Python 3.8 or later
- pip (Python package installer)
- Git (to clone the repository)

### Installation Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/amon-mr-error/jd_cv_matching.git
   cd jd_cv_matching
   ```

2. **Create and Activate a Virtual Environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate       # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Directory Structure:**

   Ensure that the `processing` folder contains the following files:
   - `parser.py`
   - `processor.py`
   - `matching.py`
   - `skills.json` (containing the skills list)

## Usage

To run the application locally using Streamlit:

```bash
streamlit run main.py
```

### How to Use the App

1. **Upload Files:**  
   - Upload a job description (PDF or DOCX) in one uploader.
   - Upload one or more candidate CVs (PDF or DOCX) in the other uploader.

2. **View Results:**  
   - The dashboard will display candidate rankings based on the combined final score.
   - You can click on a candidate’s name to view detailed information, including their extracted email.

## Project Access

The project is also accessible as a deployed Streamlit app:  
[JD/CV Matching System](https://jdcvmatching-jbcmtsfkcuw6p5tw69pqzn.streamlit.app/)

## Contributing

Contributions are welcome! If you have suggestions or improvements, please create an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m "Add new feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or suggestions, please open an issue in this repository or contact me directly at [your-email@example.com](mailto:your-email@example.com).

---

Feel free to adjust the content to match any specific details or additional instructions for your project. This README should provide a clear and complete documentation of your project’s documentation and workflow for both contributors and end-users.
