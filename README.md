🎧 Audio-to-Defect Transformer
The Audio-to-Defect Transformer is a Streamlit-based application that allows users to process audio/video files for defect detection and evaluation. It provides two primary modes of operation: Inference and Evaluation.

Table of Contents
Features
Installation
Usage
Modes of Operation
Inference Mode
Evaluation Mode
Plots and Metrics
File Structure
Future Enhancements
Features
Inference Mode: Transcribes audio/video files and generates titles and descriptions using a language model. Computes metrics like ROUGE score and semantic similarity.
Evaluation Mode: Processes audio/video files along with a ground truth file to evaluate transcription accuracy. Computes metrics such as ROUGE score, Word Error Rate (WER), and context relevance.
Interactive UI: User-friendly interface with dropdown-based mode selection.
Visualizations: Provides bar plots for metrics like ROUGE scores, semantic similarity, and more.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-repo/audio-to-defect-transformer.git
cd audio-to-defect-transformer
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Ensure ffmpeg is installed on your system:

On Ubuntu: sudo apt install ffmpeg
On macOS (with Homebrew): brew install ffmpeg
On Windows: Download and install from FFmpeg.org.
Usage
Run the application:

bash
Copy code
streamlit run app.py
Open your browser and navigate to http://localhost:8501.

Select a mode from the dropdown (Inference or Evaluation) and upload the required files.

Modes of Operation
Inference Mode
Purpose: Generate defect titles and descriptions without a ground truth file.
Steps:
Upload one or more audio/video files.
The app transcribes the files and uses a language model to generate defect titles and descriptions.
Metrics like ROUGE score and semantic similarity are computed for transcription-to-title and transcription-to-description.
Evaluation Mode
Purpose: Evaluate the accuracy of generated outputs against a ground truth file.
Steps:
Upload a ground truth Excel file and one or more audio/video files.
The app processes the files, computes metrics like ROUGE, WER, and context relevance, and compares the results against the ground truth.
Visualization of metrics is provided.
Plots and Metrics
The application generates the following visualizations:

ROUGE Scores:

Title: Transcription vs. Predicted Title
Description: Transcription vs. Predicted Description
Semantic Similarity:

Title: Transcription vs. Predicted Title
Description: Transcription vs. Predicted Description
Context Relevance:

Visualizes the relationship between transcription and generated outputs.
Metrics Computed
ROUGE Score: Measures overlap between transcription and predicted outputs.
Semantic Similarity: Calculates similarity between generated outputs and transcriptions.
Word Error Rate (WER): For evaluation mode, compares transcription with ground truth descriptions.
File Structure
plaintext
Copy code
audio-to-defect-transformer/
├── app.py               # Main application file
├── process.py           # Handles file processing and metric computation
├── visualization.py     # Handles metric visualizations
├── util.py              # Utility functions (e.g., model loading)
├── requirements.txt     # List of dependencies
├── README.md            # Documentation (this file)
└── prompt.md            # Prompt template for language model
