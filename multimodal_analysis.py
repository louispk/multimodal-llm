import streamlit as st
import pandas as pd
import re
import random
import os
from datasets import load_dataset

# Function definitions
letter_to_num = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
num_to_letter = {v: k for k, v in letter_to_num.items()}  # Reverse mapping
#pattern = re.compile(r'\b([A-E])(?:\))?\b')
pattern_with_parenthesis = re.compile(r'\b(?P<answer>[A-E])\)\b')
pattern_without_parenthesis = re.compile(r'\b(?P<answer>[A-E])\b(?!\\)')



def get_choice_letter(text, choices):
    for idx, choice in enumerate(choices):
        if choice.lower() in text.lower():
            return chr(65 + idx)  # chr(65) is 'A', chr(66) is 'B', and so on
    return None

def extract_answer(response, choices):
    match = re.search(r"Assistant:.*?\b([A-D])\b", response)
    if match:
        return match.group(1)
    
    answer_text = response.split("Assistant:", 1)[-1].strip()
    choice_letter = get_choice_letter(answer_text, choices)
    if choice_letter:
        return choice_letter
    
    return None

def is_answer_correct(row, column):
    extracted_value = letter_to_num.get(row[column], row[column])
    return row['answer'] == extracted_value

def extract_info(text):
    match = pattern.search(text)
    if match:
        answer = match.group(1)
        reasoning_index = text.rfind(answer) + len(answer)
        reasoning_text = text[:reasoning_index].strip()
        if len(reasoning_text.split()) > 10:
            return answer, reasoning_text
        return answer, None
    return None, None

def extract_info(text):
    assistant_text = text.split("Assistant:")[1]  # Splitting to get text after 'Assistant:'
    match = pattern.search(assistant_text)
    if match:
        answer = match.group('answer')
        reasoning_index = assistant_text.rfind(answer)
        reasoning_text = assistant_text[:reasoning_index].strip()
        if len(reasoning_text.split()) > 10:
            return answer, reasoning_text
        return answer, None
    return None, None

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

@st.cache_data
def load_hf_sqa():
	return pd.DataFrame(load_dataset("derek-thomas/ScienceQA", split="test"))

def load_data():
    folder_path = '/Users/louis/Documents/MA_code/scienceqa_files/'
    st.info(f"This dashboard tries to load all .csv files in the folder {folder_path} into separate dataframes")
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    success_count = 0
    error_list = []
    df_names_list = []

    for file in files:
        file_path = os.path.join(folder_path, file)
        df_name = file.split('.')[0] + '_df'
        try:
            globals()[df_name] = pd.read_csv(file_path)
            df_names_list.append(df_name)
            success_count += 1
            
        except Exception as e:
            error_list.append(f"Failed to load {file}: {str(e)}")

    if error_list:
        st.write("Errors encountered:")
        for error in error_list:
            st.write(error)
    else:
        st.success(f"All {success_count} CSV files were successfully uploaded as: {', '.join(df_names_list)}.")


def main():
    # Streamlit App
    st.title("Multimodal Annotator")

    st.image("/Users/louis/Documents/MA_code/dall_e_logo.png")

    load_data()

    sq_df = load_hf_sqa()
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    st.dataframe(sq_df)


    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("**Data Overview:**")
        st.dataframe(df.head())

        reversed_columns = list(df.columns)[::-1]
        column_to_analyze = st.selectbox("**Select the column to analyze:**", reversed_columns, index=0)

        # Apply the analysis functions
        df['extracted_answer'] = df.apply(lambda row: extract_answer(row[column_to_analyze], row['choices']), axis=1)
        #df[['answer_letter', 'reasoning']] = df[column_to_analyze].apply(lambda x: pd.Series(extract_info(x)))
        #df[['answer_letter', 'reasoning']] = df[column_to_analyze].apply(lambda x: pd.Series(extract_info(x)))
        df[['answer_letter', 'reasoning']] = df[column_to_analyze].apply(lambda x: pd.Series(extract_info(x)))


        df['is_correct'] = df.apply(lambda row: is_answer_correct(row, 'extracted_answer'), axis=1)

        if st.button("Generate Random Number"):
            st.session_state['random_number'] = random.randint(0, len(df) - 1)

        # Display a random answer if a random number has been generated
        if 'random_number' in st.session_state:
            st.write("---")

            # Display a random answer
            st.subheader("Random Answer Analysis:")
            answer_no = st.session_state['random_number']
            st.write(f"**Answer number**: {answer_no}")

            # Split the text into User and Assistant parts
            user_text, assistant_text = df[column_to_analyze][answer_no].split("Assistant:")

            # st.markdown(f"**User:**\n```\n{user_text.strip()}\n```")
            if sq_df["image"][answer_no]:
                st.image(sq_df["image"][answer_no])

            st.write(f"**User:**\n", user_text)

            # st.markdown(f"**Assistant:**\n```\n{assistant_text.strip()}\n```")
            st.write(f"**Assistant:**\n", assistant_text)
            

            st.write("---")
            st.subheader("Answer extraction")

            st.write(f"**Correct answer**: {num_to_letter[df['answer'][answer_no]]}")
            st.write(f"**Extracted answer**: {df['extracted_answer'][answer_no]}")
            st.write(f"**Regex extraction approach**: {df['answer_letter'][answer_no]}")
            st.write(f"**Extracted answer**: {df['reasoning'][answer_no]}")



        #st.write(df[column_to_analyze][349])



main()



