import streamlit as st
import pandas as pd
import re
import random
from datasets import load_dataset
import os

class MultimodalAnnotator:
    def __init__(self):
        self.df_dict = {}
        self.sq_df = self.load_hf_sqa()
        self.selected_df_names = list(self.df_dict.keys())  # Initialize with all dataframe names
        self.random_answer_no = None
    
    @st.cache_data
    def load_hf_sqa(_self):
        return pd.DataFrame(load_dataset("derek-thomas/ScienceQA", split="test"))
    
    def load_data(self, folder_path):
        files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        for file in files:
            file_path = os.path.join(folder_path, file)
            df_name = file.split('.')[0]
            try:
                self.df_dict[df_name] = pd.read_csv(file_path)
            except Exception as e:
                st.error(f"Failed to load {file}: {str(e)}")
    
    # def display_dataframes(self):
    #     #cols = st.columns(len(self.selected_df_names))
    #     num_columns = min(len(self.df_dict), 3)
    #     cols = st.columns(num_columns)
    #     self.selected_df_names = list(self.df_dict.keys())[:num_columns]  # Update selected_df_names to match the number of columns
        
    #     for i, df_name in enumerate(self.selected_df_names):
    #         df = self.df_dict[df_name]
    #         cols[i].subheader(df_name)
    #         self.display_random_answer_analysis(cols[i], df)

    def display_dataframes(self):
        num_columns = min(len(self.df_dict), 3)
        cols = st.columns(num_columns)
        
        self.selected_df_names = list(self.df_dict.keys())[:num_columns]  # Update selected_df_names to match the number of columns
        
        for i, df_name in enumerate(self.selected_df_names):
            df = self.df_dict[df_name]
            with cols[i]:
                st.subheader(df_name)
                self.display_random_answer_analysis(df)
    
    # def display_random_answer_analysis(self, col, df):
    #     if self.random_answer_no is not None and not df.empty:
    #         col.write("---")
    #         col.subheader("Random Answer Analysis:")
    #         col.write(f"**Answer number**: {self.random_answer_no}")
            
    #         # Assuming the column to analyze is known and fixed
    #         reversed_columns = list(df.columns)[::-1]
    #         column_to_analyze = st.selectbox("**Select the column to analyze:**", reversed_columns, index=0)
    #         # column_to_analyze = 'your_column_name'
            
    #         if self.random_answer_no < len(df):
    #             user_text, assistant_text = df[column_to_analyze][self.random_answer_no].split("Assistant:")
    #             if self.sq_df["image"][self.random_answer_no]:
    #                 col.image(self.sq_df["image"][self.random_answer_no])
    #             col.write(f"**User:**\n", user_text)
    #             col.write(f"**Assistant:**\n", assistant_text)
    #         else:
    #             col.write("No data available for the selected random number.")
    
    def display_random_answer_analysis(self, df):
        if self.random_answer_no is not None and not df.empty:
            st.write("---")
            st.subheader("Random Answer Analysis:")
            st.write(f"**Answer number**: {self.random_answer_no}")
            
            # Assuming the column to analyze is known and fixed
            reversed_columns = list(df.columns)[::-1]
            column_to_analyze = st.selectbox("**Select the column to analyze:**", reversed_columns, index=0)
            #column_to_analyze = 'your_column_name'
            
            if self.random_answer_no < len(df):
                user_text, assistant_text = df[column_to_analyze][self.random_answer_no].split("Assistant:")
                if self.sq_df["image"][self.random_answer_no]:
                    st.image(self.sq_df["image"][self.random_answer_no])
                st.write(f"**User:**\n", user_text)
                st.write(f"**Assistant:**\n", assistant_text)
            else:
                st.write("No data available for the selected random number.")
        
    def run(self):
        st.title("Multimodal Annotator")
        st.image("/Users/louis/Documents/MA_code/dall_e_logo.png")

        folder_path = '/Users/louis/Documents/MA_code/scienceqa_files/'
        self.load_data(folder_path)
        
        self.random_answer_no = 12
        if st.button("Generate Random Number"):
            self.random_answer_no = random.randint(0, max(len(df) for df in self.df_dict.values()) - 1)
        
        self.display_dataframes()


def extract_answer(response, choices):
    match = re.search(r"Assistant:.*?\b([A-D])\b", response)
    if match:
        return match.group(1)
    
    answer_text = response.split("Assistant:", 1)[-1].strip()
    choice_letter = get_choice_letter(answer_text, choices)
    if choice_letter:
        return choice_letter
    
    return None

def extract_info(text):
    assistant_text = text.split("Assistant:")[1]  # Splitting to get text after 'Assistant:'
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

def is_answer_correct(row, column):
    extracted_value = letter_to_num.get(row[column], row[column])
    return row['answer'] == extracted_value


# Main function
def main():
    annotator = MultimodalAnnotator()
    annotator.run()

main()
