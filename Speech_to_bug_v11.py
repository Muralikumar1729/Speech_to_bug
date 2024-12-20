import streamlit as st
import pandas as pd
import tempfile
import os
import whisper
import subprocess
from sentence_transformers import SentenceTransformer, util
from langchain_google_genai import ChatGoogleGenerativeAI
from jiwer import wer
from rouge_score import rouge_scorer

# API Key and Prompt Path
API_KEY = 'AIzaSyAeY-JZQUTeI8kCgVt1Ey_sufpvvjPB9p0'  # Replace with your actual API key
PROMPT_FILE_PATH = "prompt.md"  # Ensure this file is in the same directory as the script

# Load Models
whisper_model = whisper.load_model("small")
semantic_similarity_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=API_KEY,
)

# Evaluation Metrics Functions
def calculate_wer(reference, hypothesis):
    return wer(reference, hypothesis)

def calculate_semantic_similarity(reference, hypothesis):
    embeddings = semantic_similarity_model.encode([reference, hypothesis])
    return util.cos_sim(embeddings[0], embeddings[1]).item()

def calculate_rouge(reference, hypothesis):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    return scores

# Clean LLM Output
def clean_llm_output(text):
    return text.replace("Expected Defect Title: ", "").replace("Expected Defect Description: ", "").strip()

# Process File
def process_file(file_path, model, llm, prompt_template, ground_truth):
    temp_audio = os.path.basename(file_path) + ".wav"
    extract_audio(file_path, temp_audio)
    result = model.transcribe(temp_audio)
    transcription = result.get("text", "")
    os.remove(temp_audio)

    # Generate Defect Title and Description
    formatted_prompt = prompt_template.format(transcription=transcription)
    response = llm.invoke(formatted_prompt)
    output_text = response.content.split("\n", 1)
    predicted_title = clean_llm_output(output_text[0] if output_text else "")
    predicted_description = clean_llm_output(output_text[1] if len(output_text) > 1 else "")

    # Extract actual values from ground truth
    actual_transcription = str(ground_truth["Recorded Defect Description"])
    actual_title = str(ground_truth["Expected Defect Title"])
    actual_description = str(ground_truth["Expected Defect Description"])

    # Evaluate Metrics
    rouge_scores = calculate_rouge(actual_transcription, transcription)
    semantic_similarity_title = calculate_semantic_similarity(actual_title, predicted_title)
    semantic_similarity_description = calculate_semantic_similarity(actual_description, predicted_description)
    word_error_rate = calculate_wer(actual_transcription, transcription)

    return {
        "File Name": ground_truth["FileName"],
        "Predicted Transcription": transcription,
        "Generated Defect Title": predicted_title,
        "Generated Defect Description": predicted_description,
        "Actual Transcription": actual_transcription,
        "ROUGE-1": rouge_scores['rouge1'].fmeasure,
        "ROUGE-2": rouge_scores['rouge2'].fmeasure,
        "ROUGE-L": rouge_scores['rougeL'].fmeasure,
        "WER": word_error_rate,
        "Actual Title": actual_title,
        "Semantic Similarity Title": semantic_similarity_title,
        "Actual Description": actual_description,
        "Semantic Similarity Description": semantic_similarity_description,
    }

# Extract Audio
def extract_audio(input_path, output_path):
    command = f'ffmpeg -i "{input_path}" -ab 256k -ar 48000 -vn -y "{output_path}"'
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Main App Logic
def main():
    # Set Streamlit to use wide mode for the layout
    st.set_page_config(page_title="Audio-to-Defect Transformer", layout="wide", initial_sidebar_state="expanded")

    # UI title and description
    st.title("🎧 Audio-to-Defect Transformer")
    st.markdown("### Transform audio recordings into actionable defect insights using advanced AI models.")

    # Sidebar for file uploads
    with st.sidebar:
        st.header("🔧 Configuration")
        st.markdown("Upload the required files and click 'Process and Evaluate' to generate and evaluate defect details.")

        # File upload widgets
        excel_file = st.file_uploader("Upload Ground Truth Excel File", type=["xlsx"], help="Upload the Excel file containing the ground truth data.")
        uploaded_files = st.file_uploader("Upload Audio/Video Files", type=["mp4", "wav", "mp3"], accept_multiple_files=True, help="Upload one or more audio/video files.")

    # Process and Evaluate Button
    if st.button("🔄 Process and Evaluate", key="process_button"):
        if excel_file and uploaded_files:
            ground_truth_df = pd.read_excel(excel_file)
            prompt_template = open(PROMPT_FILE_PATH).read()

            results = []
            with tempfile.TemporaryDirectory() as temp_dir:
                for file in uploaded_files:
                    original_file_name = file.name.split('.')[0]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file.name) as temp_file:
                        temp_file.write(file.getvalue())
                        ground_truth = ground_truth_df[ground_truth_df["FileName"] == original_file_name].iloc[0]
                        res = process_file(temp_file.name, whisper_model, llm, prompt_template, ground_truth)
                        if res:
                            results.append(res)

            # Split Results into Tables
            df = pd.DataFrame(results)

            # Display Results in Tables (Professional Layout)
            st.subheader("Predicted Transcriptions and Defect Details")
            st.dataframe(df[["File Name", "Predicted Transcription", "Generated Defect Title", "Generated Defect Description"]], width=1000)

            st.subheader("Transcription Metrics")
            st.dataframe(df[["File Name", "Actual Transcription", "Predicted Transcription", "ROUGE-1", "ROUGE-2", "ROUGE-L", "WER"]], width=1000)

            st.subheader("Defect Title Similarity")
            st.dataframe(df[["File Name", "Actual Title", "Generated Defect Title", "Semantic Similarity Title"]], width=1000)

            st.subheader("Defect Description Similarity")
            st.dataframe(df[["File Name", "Actual Description", "Generated Defect Description", "Semantic Similarity Description"]], width=1000)

            # Allow users to download the result as a CSV file
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="defect_evaluation_results.csv",
                mime="text/csv",
            )
        else:
            st.error("Please upload both the ground truth Excel file and the audio/video files.")

if __name__ == "__main__":
    main()
