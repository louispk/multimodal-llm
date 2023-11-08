# README for the Multimodal Output Analysis Tool (MOAT)

## Overview

The Multimodal Output Analysis Tool (MOAT) is a Streamlit-based application designed to assist researchers and practitioners in analyzing and understanding the outputs from multimodal Large Language Models (LLMs) within the context of the ScienceQA dataset. It provides functionalities to load data, display questions with their associated answer choices and images, and perform answer analysis with extracted reasoning.

## Features

- **Load Data**: Automatically loads the ScienceQA dataset and any `.csv` data files from a specified folder into dataframes for analysis.
- **Display Questions**: Shows the question text, answer choices, and associated images from the dataset.
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

4. Run the Streamlit application:
```bash
streamlit run app.py
```

## Usage

Upon launching MOAT, you will be greeted with a simple user interface with the following components:

- **Header**: Displays the title and logo of the tool.
- **Data Loader**: Automatically loads the required datasets and prepares them for analysis.
- **Random Number Generator**: Allows you to randomly select an entry from the dataset for analysis.
- **Number Input**: Enables you to analyze a specific entry by entering its number.
- **Answer Display**: Shows the details of the question, answer choices, images, and the analysis of the selected entry.
- **Statistics**: Presents overall statistics and visualizations based on the current data loaded.

## Customization

The tool is designed to be flexible and can be customized to suit different datasets and requirements. You can modify the source code to include different datasets, add new analysis metrics, or adjust the visualizations.

## Contributing

We welcome contributions to MOAT! If you have suggestions for improvements or new features, feel free to fork the repository, make changes, and submit a pull request. Please ensure that your code adheres to the project's coding standards and include documentation for any new features.

## License

Please include the appropriate license information here.

## Support

For support, please open an issue on the GitHub repository, and a maintainer will assist you.

---

MOAT is a powerful tool for analyzing multimodal data and provides a user-friendly interface to facilitate the understanding of complex LLM outputs. We hope it assists you in your research and development efforts!
