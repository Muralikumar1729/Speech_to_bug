import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def plot_comparisons(df):
    st.subheader("📊 Comparison Plots")

    # Create a figure and axis for all subplots
    fig, axs = plt.subplots(2, 2, figsize=(14, 12))  # You can adjust the grid size as needed
    axs = axs.flatten()  # Flatten to make indexing easier

    # Plot for Actual Title vs Predicted Title
    sns.barplot(
        x="File Name", 
        y="NLI Title Score", 
        data=df, 
        color="blue", 
        alpha=0.6, 
        ax=axs[0]
    )
    for bar, label in zip(axs[0].patches, df["NLI Title Label"]):
        axs[0].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            label,
            ha="center",
            va="bottom",
            fontsize=9
        )
    axs[0].set_xlabel("File Name")
    axs[0].set_ylabel("NLI Score")
    axs[0].set_title("NLI Score: Actual Transcription vs. Actual Title")

    # Plot for Actual Description vs Predicted Description
    sns.barplot(
        x="File Name", 
        y="NLI Description Score", 
        data=df, 
        color="orange", 
        alpha=0.6, 
        ax=axs[1]
    )
    for bar, label in zip(axs[1].patches, df["NLI Description Label"]):
        axs[1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            label,
            ha="center",
            va="bottom",
            fontsize=9
        )
    axs[1].set_xlabel("File Name")
    axs[1].set_ylabel("NLI Score")
    axs[1].set_title("NLI Score: Actual Transcription vs. Actual Description")

    # Plot for Predicted Title
    sns.barplot(
        x="File Name", 
        y="NLI Title Score", 
        data=df, 
        color="green", 
        alpha=0.6, 
        ax=axs[2]
    )
    for bar, label in zip(axs[2].patches, df["NLI Title Label"]):
        axs[2].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            label,
            ha="center",
            va="bottom",
            fontsize=9
        )
    axs[2].set_xlabel("File Name")
    axs[2].set_ylabel("NLI Score")
    axs[2].set_title("NLI Score: Actual Transcription vs. Predicted Title")

    # Plot for Predicted Description
    sns.barplot(
        x="File Name", 
        y="NLI Description Score", 
        data=df, 
        color="purple", 
        alpha=0.6, 
        ax=axs[3]
    )
    for bar, label in zip(axs[3].patches, df["NLI Description Label"]):
        axs[3].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            label,
            ha="center",
            va="bottom",
            fontsize=9
        )
    axs[3].set_xlabel("File Name")
    axs[3].set_ylabel("NLI Score")
    axs[3].set_title("NLI Score: Actual Transcription vs. Predicted Description")

    # Adjust layout and display all plots
    plt.tight_layout()
    st.pyplot(fig)

