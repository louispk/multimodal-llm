# README for the Multimodal Output Analysis Tool (MOAT)

## Overview

The Multimodal Output Analysis Tool (MOAT) is a Streamlit-based application designed to assist researchers and practitioners in analyzing and understanding the outputs from multimodal Large Language Models (MLLMs) within the context of the ScienceQA (or other Huggingface) dataset. It provides functionalities to load data, display questions with their associated answer choices and images, and perform answer analysis with extracted reasoning.

## Features

- **Load Data**: Automatically loads the ScienceQA dataset (any other can be specified in the script) and any `.csv` data files from a the Input_files folder into dataframes for analysis.
- **Display Questions**: Shows the question text, answer choices, and associated images from the dataset. It creates as many columns as there are usable .csv files in the folder, so if you want 25 columns à 10px width, feel free.
- **Answer Analysis**: Provides a detailed analysis of the answers including the extracted answer, extracted reasoning, and comparison with the correct answer.
- **Statistics Calculation**: Calculates and displays statistics like the length of the dataframe, the number of correct matches, and the number of extracted reasonings.
- **Data Visualization**: Plots the number of correct matches and the relative accuracy for each dataframe.
- **Interactivity**: Users can generate random numbers to analyze random entries or input specific numbers for targeted analysis.

## Installation

To run MOAT, you need to have Python installed on your machine along with the necessary libraries. Here are the steps to set up the application:

1. Clone the GitHub repository:
```bash
git clone <repository-url>
```

2. Navigate to the cloned repository directory.

3. Install the required packages using pip:
```bash
pip install -r requirements.txt
```

4. Insert your output .csv files into the ```Input_files``` folder

5. Run the Streamlit application:
```bash
streamlit run multimodal_annotator.py
```

## Customization

The tool is designed to be flexible and can be customized to suit different datasets and requirements. You can modify the source code to include different datasets, add new analysis metrics, or adjust the visualizations.


## License

Moat is distribute under the MIT license.

## Support

For support, please open an issue on the GitHub repository, and a maintainer (me) will (maybe) assist you.


