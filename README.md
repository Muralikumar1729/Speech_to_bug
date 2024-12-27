# 🎧 Audio-to-Defect Transformer

The **Audio-to-Defect Transformer** is a Streamlit-based application that allows users to process audio/video files for defect detection and evaluation. It provides two primary modes of operation: **Inference** and **Evaluation**.

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Modes of Operation](#modes-of-operation)
    - [Inference Mode](#inference-mode)
    - [Evaluation Mode](#evaluation-mode)
5. [Plots and Metrics](#plots-and-metrics)
6. [File Structure](#file-structure)
7. [Future Enhancements](#future-enhancements)

## Features

- **Inference Mode**: Transcribes audio/video files and generates titles and descriptions using a language model. Computes metrics like ROUGE score and semantic similarity.
- **Evaluation Mode**: Processes audio/video files along with a ground truth file to evaluate transcription accuracy. Computes metrics such as ROUGE score, Word Error Rate (WER), and context relevance.
- **Interactive UI**: User-friendly interface with dropdown-based mode selection.
- **Visualizations**: Provides bar plots for metrics like ROUGE scores, semantic similarity, and more.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/audio-to-defect-transformer.git
    cd audio-to-defect-transformer
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure `ffmpeg` is installed on your system:
    - On Ubuntu: `sudo apt install ffmpeg`
    - On macOS (with Homebrew): `brew install ffmpeg`
    - On Windows: Download and install from [FFmpeg.org](https://ffmpeg.org/).

## Usage

1. Run the application:
    ```bash
    streamlit run app.py
    ```

2. Open your browser and navigate to `http://localhost:8501`.

3. Select a mode from the dropdown (**Inference** or **Evaluation**) and upload the required files.

## Modes of Operation

### Inference Mode
- **Purpose**: Generate defect titles and descriptions without a ground truth file.
- **Steps**:
  1. Upload one or more audio/video files.
  2. The app transcribes the files and uses a language model to generate defect titles and descriptions.
  3. Metrics like ROUGE score and semantic similarity are computed for transcription-to-title and transcription-to-description.

### Evaluation Mode
- **Purpose**: Evaluate the accuracy of generated outputs against a ground truth file.
- **Steps**:
  1. Upload a ground truth Excel file and one or more audio/video files.
  2. The app processes the files, computes metrics like ROUGE, WER, and context relevance, and compares the results against the ground truth.
  3. Visualization of metrics is provided.

## Plots and Metrics

The application generates the following visualizations:

1. **ROUGE Scores**:
   - Title: Transcription vs. Predicted Title
   - Description: Transcription vs. Predicted Description

2. **Semantic Similarity**:
   - Title: Transcription vs. Predicted Title
   - Description: Transcription vs. Predicted Description

3. **Context Relevance**:
   - Visualizes the relationship between transcription and generated outputs.

### Metrics Computed
- **ROUGE Score**: Measures overlap between transcription and predicted outputs.
- **Semantic Similarity**: Calculates similarity between generated outputs and transcriptions.
- **Word Error Rate (WER)**: For evaluation mode, compares transcription with ground truth descriptions.

## File Structure

```plaintext
audio-to-defect-transformer/
├── app.py               # Main application file
├── process.py           # Handles file processing and metric computation
├── visualization.py     # Handles metric visualizations
├── util.py              # Utility functions (e.g., model loading)
├── requirements.txt     # List of dependencies
├── README.md            # Documentation (this file)
└── prompt.md            # Prompt template for language model
