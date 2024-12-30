import streamlit as st
import pandas as pd
import tempfile
from process_v2 import process_file, process_inference
from visualization_v3 import plot_comparisons
import os

def print_tables(df,mode):
    
    st.subheader("Predicted Transcriptions and Defect Details")
    st.dataframe(df[["File Name", "Predicted Transcription", "Generated Defect Title", "Generated Defect Description"]], width=1000)
    if mode=="Evaluation":
        st.subheader("Transcription Metrics")
        st.dataframe(df[["File Name", "Actual Transcription", "Predicted Transcription", "ROUGE-1", "ROUGE-2", "ROUGE-L", "WER"]], width=1000)

        st.subheader("Defect Title Metrics")
        st.dataframe(df[["File Name", "Actual Title", "Generated Defect Title", "Semantic Similarity Title", "Context Relevancy Title", "NLI Title Label actual", "NLI Title Score actual","NLI Title Label predicted","NLI Title Score predicted"]], width=1000)

        st.subheader("Defect Description Metrics")
        st.dataframe(df[["File Name", "Actual Description", "Generated Defect Description", "Semantic Similarity Description", "Context Relevancy Description", "NLI Description Label actual", "NLI Description Score actual", "NLI Description Label predicted","NLI Description Score predicted"]], width=1000)
    else:
        st.subheader("Defect Title Metrics")
        st.dataframe(df[["File Name", "Generated Defect Title", "Context Relevancy Title", "NLI Title Label predicted", "NLI Title Score predicted"]], width=1000)

        st.subheader("Defect Description Metrics")
        st.dataframe(df[["File Name",  "Generated Defect Description", "Context Relevancy Description", "NLI Description Label predicted", "NLI Description Score predicted"]], width=1000)



def main():
    # Set Streamlit to use wide mode for the layout
    st.set_page_config(page_title="Audio-to-Defect Transformer", layout="wide", initial_sidebar_state="expanded")

    # Dropdown for selecting mode
    st.title("🎧 Audio-to-Defect Transformer")
    st.markdown("### Choose between Inference or Evaluation modes.")

    mode = st.selectbox("Select Mode", options=["Inference", "Evaluation"], index=0)

    if mode == "Inference":
        st.header("Inference Mode")
        st.markdown("Upload audio or video files to generate metrics without ground truth.")
        
        uploaded_files = st.file_uploader(
            "Upload Audio/Video Files", 
            type=["mp4", "wav", "mp3"], 
            accept_multiple_files=True, 
            help="Upload one or more audio/video files."
        )

        if st.button("🔄 Process and Evaluate", key="process_button_inference"):
            if uploaded_files:
                prompt_template = open("prompt.md").read()
                results = []
                with tempfile.TemporaryDirectory() as temp_dir:
                    for file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=file.name) as temp_file:
                            temp_file.write(file.getvalue())
                            res = process_inference(temp_file.name, file.name, prompt_template)
                            if res:
                                results.append(res)

                # Create DataFrame
                df = pd.DataFrame(results)

                # Display Results in Tables
                #st.subheader("Inference Results")
                #st.dataframe(df)
                print_tables(df,mode)
                # Generate plots
                plot_comparisons(df,True)

                # Allow users to download the result as a CSV file
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Inference Results as CSV",
                    data=csv,
                    file_name="inference_results.csv",
                    mime="text/csv",
                )
            else:
                st.error("Please upload audio/video files.")

    elif mode == "Evaluation":
        st.header("Evaluation Mode")
        st.markdown("Upload audio/video files along with a ground truth Excel file to evaluate metrics.")

        excel_file = st.file_uploader(
            "Upload Ground Truth Excel File", 
            type=["xlsx"], 
            help="Upload the Excel file containing the ground truth data."
        )
        uploaded_files = st.file_uploader(
            "Upload Audio/Video Files", 
            type=["mp4", "wav", "mp3"], 
            accept_multiple_files=True, 
            help="Upload one or more audio/video files."
        )

        if st.button("🔄 Process and Evaluate", key="process_button_evaluation"):
            if excel_file and uploaded_files:
                ground_truth_df = pd.read_excel(excel_file)
                prompt_template = open("prompt.md").read()

                results = []
                with tempfile.TemporaryDirectory() as temp_dir:
                    for file in uploaded_files:
                        original_file_name = file.name.split('.')[0]
                        with tempfile.NamedTemporaryFile(delete=False, suffix=file.name) as temp_file:
                            temp_file.write(file.getvalue())
                            ground_truth = ground_truth_df[ground_truth_df["FileName"] == original_file_name].iloc[0]
                            res = process_file(temp_file.name, ground_truth, prompt_template)
                            if res:
                                results.append(res)

                # Create DataFrame
                df = pd.DataFrame(results)

                # Display Results in Tables
                #st.subheader("Evaluation Results")
                #st.dataframe(df)
                print_tables(df,mode)
                # Generate plots
                plot_comparisons(df)

                # Allow users to download the result as a CSV file
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Evaluation Results as CSV",
                    data=csv,
                    file_name="evaluation_results.csv",
                    mime="text/csv",
                )
            else:
                st.error("Please upload both the ground truth Excel file and the audio/video files.")

if __name__ == "__main__":
    main()
