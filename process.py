import whisper
from sentence_transformers import SentenceTransformer, util
from jiwer import wer
from rouge_score import rouge_scorer
from langchain_google_genai import ChatGoogleGenerativeAI
from transformers import pipeline
import tempfile
import os
import streamlit as st

# Initialize Models
whisper_model = whisper.load_model("small")
semantic_similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
API_KEY = 'AIz-'
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

def process_inference(file_path, file_name, prompt_template):
    
    # Transcribe audio to text
    result = whisper_model.transcribe(file_path)
    transcription = result.get("text", "")

    # Generate Defect Title and Description
    formatted_prompt = prompt_template.format(transcription=transcription)
    response = llm.invoke(formatted_prompt)
    output_text = response.content.split("\n", 1)
    predicted_title = clean_llm_output(output_text[0] if output_text else "")
    predicted_description = clean_llm_output(output_text[1] if len(output_text) > 1 else "")

    # Evaluate Metrics
    
    context_relevancy_title = calculate_semantic_similarity(transcription, predicted_title)
    context_relevancy_desc = calculate_semantic_similarity(transcription, predicted_description)
    
    nli_pipeline = pipeline("text-classification", model="roberta-large-mnli")
    
    NLI_title = nli_pipeline(f"{transcription} \n {predicted_title}")[0]
    NLI_desc = nli_pipeline(f"{transcription} \n {predicted_description}")[0]
    # Populate DataFrame with placeholders for metrics not computed in Inference mode
    return {
        "File Name": file_name,
        "Predicted Transcription": transcription,
        "Generated Defect Title": predicted_title,
        "Generated Defect Description": predicted_description,
        "Context Relevancy Title": context_relevancy_title,
        "Context Relevancy Description": context_relevancy_desc,
        # Add placeholders for metrics not computed
        "NLI Title Label predicted": NLI_title['label'],
        "NLI Title Score predicted": NLI_title['score'],
        "NLI Description Label predicted": NLI_desc['label'],
        "NLI Description Score predicted": NLI_desc['score']
    }



# Process File
def process_file(file_path, ground_truth, prompt_template):
    # Transcribe audio to text
    result = whisper_model.transcribe(file_path)
    transcription = result.get("text", "")

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
    context_relevancy_title = calculate_semantic_similarity(transcription, predicted_title)
    context_relevancy_desc = calculate_semantic_similarity(transcription, predicted_description)
    nli_pipeline = pipeline("text-classification", model="facebook/bart-large-mnli")
    NLI_title_pred = nli_pipeline(f"{actual_transcription} \n {predicted_title}")[0]
    NLI_desc_pred = nli_pipeline(f"{actual_transcription} \n {predicted_description}")[0]
    NLI_title_act = nli_pipeline(f"{actual_transcription} \n {actual_title}")[0]
    NLI_desc_act = nli_pipeline(f"{actual_transcription} \n {actual_description}")[0]
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
        "Context Relevancy Title": context_relevancy_title,
        "Context Relevancy Description": context_relevancy_desc,
        "NLI Title Label actual": NLI_title_act['label'],
        "NLI Title Score actual": NLI_title_act['score'],
        "NLI Description Label actual": NLI_desc_act['label'],
        "NLI Description Score actual": NLI_desc_act['score'],
        "NLI Title Label predicted": NLI_title_pred['label'],
        "NLI Title Score predicted": NLI_title_pred['score'],
        "NLI Description Label predicted": NLI_desc_pred['label'],
        "NLI Description Score predicted": NLI_desc_pred['score']
    }

