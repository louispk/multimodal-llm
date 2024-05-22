import streamlit as st
import pandas as pd
import random
from datasets import load_dataset
import os
import re
import matplotlib.pyplot as plt
from typing import Tuple, Dict, List, Optional


class MultimodalAnnotator:
    """A class to annotate and analyze multimodal outputs from a dataset."""
    
    def __init__(self):
        self.df_dict: Dict[str, pd.DataFrame] = {}
        self.sq_df: pd.DataFrame = self.load_hf_sqa()
        self.random_answer_no: int = 1
    
    @st.cache_data
    def load_hf_sqa(_self) -> pd.DataFrame:
        """Loads a ScienceQA dataset from the Hugging Face datasets."""
        return pd.DataFrame(load_dataset("derek-thomas/ScienceQA", split="test"))
    
    def load_data(self, folder_path: str) -> None:
        """Loads data files from the specified folder path into dataframes."""
        files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        for file in files:
            file_path = os.path.join(folder_path, file)
            df_name = file.split('.')[0]
            try:
                self.df_dict[df_name] = pd.read_csv(file_path)
            except Exception as e:
                st.error(f"Failed to load {file}: {str(e)}")

    def show_answer(self) -> None:
        """Displays the question, choices, image, and answer analysis."""
        st.subheader("Question")
        st.info(self.sq_df["question"][self.random_answer_no])

        st.subheader("Answer Choices")
        choices = self.sq_df["choices"][self.random_answer_no]
        if choices:
            lettered_choices = ''.join(f"{chr(ord('A') + idx)}) {choice}<br>"
                                     for idx, choice in enumerate(choices))
            st.markdown(lettered_choices, unsafe_allow_html=True)

        st.subheader("Image")
        image = self.sq_df["image"][self.random_answer_no]
        if image:
            st.image(image)
        else:
            st.write("This question contains no image")

        st.subheader("Answer Analysis")

    def display_dataframes(self):
        num_columns = min(len(self.df_dict), 3)
        cols = st.columns(num_columns)
        
        for i, (df_name, df) in enumerate(self.df_dict.items()):
            if i >= num_columns:
                break
            
            with cols[i]:
                st.write(df_name)
                self.display_random_answer_analysis(df, df_name)
    
    def display_random_answer_analysis(self, df, df_name, column_to_analyze): 
           if self.random_answer_no is not None and not df.empty:
            st.write("---")
            st.subheader("Closer look:")
            st.write(f"**Answer number**: {self.random_answer_no}")
            
            reversed_columns = list(df.columns)[::-1]
            column_to_analyze = st.selectbox(f"**Select the column to analyze in {df_name}:**", reversed_columns, index=0)
            
            if self.random_answer_no < len(df):
                response = df[column_to_analyze][self.random_answer_no]
                self.display_additional_info(response)
                user_text, assistant_text = response.split("Assistant:")
                if self.sq_df["image"][self.random_answer_no]:
                    st.image(self.sq_df["image"][self.random_answer_no])
                st.write(f"**User:**\n", user_text)
                st.write(f"**Assistant:**\n", assistant_text)
                
                
            else:
                st.write("No data available for the selected random number.")
    
    def display_additional_info(self, response):
        answer = self.extract_answer(response)
        st.write(f"**Extracted Answer:** {answer}")
        
        answer, reasoning = self.extract_info(response)
        st.write(f"**Ext. Answer Method 2:** {answer}")

        # st.write(f"**Correct Answer:** {self.sq_df.answer[self.random_answer_no]}")
        correct_answer_number = self.sq_df['answer'][self.random_answer_no]
        # Subtract 1 to make it 0-indexed and then convert to a letter
        correct_answer_letter = chr(ord('A') + correct_answer_number - 1)

        st.write(f"**Correct Answer:** {correct_answer_letter})")
        if reasoning:
            st.write(f"**Extracted Reasoning:** {reasoning}")
    
    def extract_answer(self, response):
        if not isinstance(response, str):
            # If the response is not a string, return None or an appropriate value
            return None
        match = re.search(r"Assistant:.*?\b([A-D])\b", response)
        if match:
            return match.group(1)
        
        answer_text = response.split("Assistant:", 1)[-1].strip()
        # Assuming choices are available in the response
        choices = re.findall(r"\b([A-D])\b", answer_text)
        choice_letter = self.get_choice_letter(answer_text, choices)
        if choice_letter:
            return choice_letter
        
        return None

    def extract_info(self, text):
        assistant_text = text.split("Assistant:")[1]
        pattern_with_parenthesis = re.compile(r"\((?P<answer>[A-D])\)")
        pattern_without_parenthesis = re.compile(r"(?P<answer>[A-D])")
        
        match = pattern_with_parenthesis.search(assistant_text)
        if not match:
            match = pattern_without_parenthesis.search(assistant_text)
        if match:
            answer = match.group('answer')
            reasoning_index = assistant_text.rfind(answer)
            reasoning_text = assistant_text[:reasoning_index].strip()
            if len(reasoning_text.split()) > 10:
                return answer, reasoning_text
            return answer, None
        return None, None
    
    def get_choice_letter(self, answer_text, choices):
        for choice in choices:
            if choice in answer_text:
                return choice
        return None


    def calculate_statistics(self, df, correct_answers, response_column_name):
        # Calculate the length of the dataframe
        length_of_dataframe = len(df)
        
        # Initialize a count for correct matches and extracted reasonings
        correct_match_count = 0
        extracted_reasoning_count = 0
        correct_answer_indices = []

        # Iterate through the dataframe
        for index, row in df.iterrows():
            if response_column_name in df.columns:
                response = row[response_column_name]
                extracted_answer, extracted_reasoning = self.extract_info(response)
                if extracted_answer is not None:
                    extracted_answer_index = ord(extracted_answer) - ord('A') + 1
                    if correct_answers[index] == extracted_answer_index:
                        correct_match_count += 1
                        correct_answer_indices.append(index)
                if extracted_reasoning:
                    extracted_reasoning_count += 1
            else:
                st.error(f"The column {response_column_name} does not exist in the dataframe.")
                break
        
        return length_of_dataframe, correct_match_count, extracted_reasoning_count



    def display_dataframes(self):
        num_columns = min(len(self.df_dict), 3)
        cols = st.columns(num_columns)

        # Create placeholders for each metric in each column to ensure alignment
        length_placeholders = [cols[i].empty() for i in range(num_columns)]
        match_placeholders = [cols[i].empty() for i in range(num_columns)]
        reasoning_placeholders = [cols[i].empty() for i in range(num_columns)]  # Placeholder for reasoning counts

        # Store lengths, match counts, and reasoning counts
        lengths = []
        match_counts = []
        reasoning_counts = []  # To store reasoning counts
        
        for i, (df_name, df) in enumerate(self.df_dict.items()):
            if i >= num_columns:
                break

            with cols[i]:
                st.write(df_name)
                reversed_columns = list(df.columns)[::-1]
                column_to_analyze = st.selectbox(f"Select the column to analyze in {df_name}:", reversed_columns, index=0)

                # Calculate statistics
                length_of_df, correct_match_count, extracted_reasoning_count = self.calculate_statistics(df, self.sq_df['answer'], column_to_analyze)
                lengths.append(length_of_df)
                match_counts.append(correct_match_count)
                reasoning_counts.append(extracted_reasoning_count)  # Append the reasoning count

                # Placeholder for displaying random answer analysis
                self.display_random_answer_analysis(df, df_name, column_to_analyze)

        # Now display the metrics at the same height
        for i, (length_of_df, correct_match_count, extracted_reasoning_count) in enumerate(zip(lengths, match_counts, reasoning_counts)):
            if i < num_columns:  # Check to avoid index error
                length_placeholders[i].metric(label="Length of Dataframe", value=length_of_df)
                match_placeholders[i].metric(label="Correct Matches", value=correct_match_count)
                reasoning_placeholders[i].metric(label="Extracted Reasonings", value=extracted_reasoning_count)  # Display the reasoning count


    def plot_correct_matches(self, df_names, match_counts):
        fig, ax = plt.subplots()
        ax.bar(df_names, match_counts, color='skyblue')
        ax.set_xlabel('Dataframes', fontsize=12)
        ax.set_ylabel('Correct Matches', fontsize=12)
        ax.set_title('Number of Correct Matches per Dataframe', fontsize=14)
        ax.set_xticklabels(df_names, rotation=45, ha='right')
        plt.tight_layout()

        st.pyplot(fig)


    def run(self) -> None:
        """Runs the main application."""
        st.title("Multimodal Output Analysis Tool")
        st.image("moat_logo.png", width=300)

        st.write("The Multimodal Output Analysis Tool (MOAT) helps analyze and understand the output of a Multimodal LLM.")
        st.write("--------")
        folder_path = '/Users/louis/Documents/MA_code/multimodal-llm/scienceqa_files/'
        self.load_data(folder_path)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate Random Number"):
                self.random_answer_no = random.randint(0, len(self.sq_df) - 1)

        with col2:
            input_number = st.text_input("Enter a number:")
            if input_number:
                try:
                    input_number = int(input_number)
                    if 0 <= input_number < len(self.sq_df):
                        self.random_answer_no = input_number
                    else:
                        st.error(f"Number out of range. Please enter a number between 0 and {len(self.sq_df) - 1}.")
                except ValueError:
                    st.error("Please enter a valid number.")

        self.show_answer()
        self.display_dataframes()

        st.write("------")
        st.subheader("Statistics")
        df_names = list(self.df_dict.keys())
        match_counts = [self.calculate_statistics(self.df_dict[df_name], self.sq_df['answer'], column_to_analyze)[1] for df_name in df_names]
        
        self.plot_correct_matches(df_names, match_counts)

        st.write(self.sq_df.answer)

def main():
    annotator = MultimodalAnnotator()
    annotator.run()

if __name__ == "__main__":
    main()
