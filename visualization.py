import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def plot_comparisons(df, is_inference=False):
    st.subheader("📊 Comparison Plots")

    if is_inference:
        st.markdown("### Inference Mode: Predicted Scores Only")

        # Plot for Predicted NLI Title Scores
        if "NLI Title Score predicted" in df.columns:
            st.markdown("#### NLI Title Scores (Predicted)")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(
                x="File Name",
                y="NLI Title Score predicted",
                data=df,
                color="blue",
                alpha=0.6,
                ax=ax
            )
            ax.set_xlabel("File Name")
            ax.set_ylabel("NLI Title Score (Predicted)")
            ax.set_title("NLI Title Score: Predicted")
            st.pyplot(fig)

        # Plot for Predicted NLI Description Scores
        if "NLI Description Score predicted" in df.columns:
            st.markdown("#### NLI Description Scores (Predicted)")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(
                x="File Name",
                y="NLI Description Score predicted",
                data=df,
                color="green",
                alpha=0.6,
                ax=ax
            )
            ax.set_xlabel("File Name")
            ax.set_ylabel("NLI Description Score (Predicted)")
            ax.set_title("NLI Description Score: Predicted")
            st.pyplot(fig)

    else:
        st.markdown("### Evaluation Mode: Comparison of Actual and Predicted Scores")

        # Plot for NLI Title Scores (Actual vs Predicted)
        if "NLI Title Score actual" in df.columns and "NLI Title Score predicted" in df.columns:
            st.markdown("#### NLI Title Scores (Actual vs Predicted)")
            fig, ax = plt.subplots(figsize=(10, 6))
            df_melted = df.melt(
                id_vars=["File Name"],
                value_vars=["NLI Title Score actual", "NLI Title Score predicted"],
                var_name="Score Type",
                value_name="NLI Title Score"
            )
            sns.barplot(
                x="File Name",
                y="NLI Title Score",
                hue="Score Type",
                data=df_melted,
                ax=ax
            )
            ax.set_xlabel("File Name")
            ax.set_ylabel("NLI Title Score")
            ax.set_title("NLI Title Score: Actual vs Predicted")
            st.pyplot(fig)

        # Plot for NLI Description Scores (Actual vs Predicted)
        if "NLI Description Score actual" in df.columns and "NLI Description Score predicted" in df.columns:
            st.markdown("#### NLI Description Scores (Actual vs Predicted)")
            fig, ax = plt.subplots(figsize=(10, 6))
            df_melted = df.melt(
                id_vars=["File Name"],
                value_vars=["NLI Description Score actual", "NLI Description Score predicted"],
                var_name="Score Type",
                value_name="NLI Description Score"
            )
            sns.barplot(
                x="File Name",
                y="NLI Description Score",
                hue="Score Type",
                data=df_melted,
                ax=ax
            )
            ax.set_xlabel("File Name")
            ax.set_ylabel("NLI Description Score")
            ax.set_title("NLI Description Score: Actual vs Predicted")
            st.pyplot(fig)
