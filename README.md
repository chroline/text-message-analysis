# Exploring Personal Communication Patterns with Data Science and NLP

This project explores patterns in personal text messaging behavior using data science and natural language processing (NLP) techniques. Leveraging libraries such as Pandas, Numpy, and NLTK, and visualizing the results with Matplotlib, this project aims to gain insights into communication styles and texting habits.

To see all the visualizations, view the [`visualizations.ipynb` notebook file](https://github.com/chroline/text-message-analysis/blob/main/visualizations.ipynb).

## Technologies Used

- **Pandas**: Data manipulation and analysis.
- **Numpy**: Numerical computing.
- **NLTK**: Natural language processing.
- **Matplotlib**: Data visualization.

## Data Collection

The dataset I used consists of my own text messages exported from iMessage. The data includes timestamps, message content, and sender information.

To generate your own dataset, run the `generate_dataset.py` file as a super-user on macOS. This should produce an `imessages.jsonl` file consisting of all of your messages.

### Preprocessing

I transform the raw text message data in the `data_preparation.ipynb` notebook. The transformations I produce are:

- localize the message timestamp
- anonymize the sender information
- extract emojis

I save this transformed data to `all_texts.pkl`, which is then utilized in the visualizations notebook.

## Data Visualization

Using Matplotlib, I create various graphs and charts to visualize the data. All of these visualizations are located in the `visualizations.ipynb` notebook.

## Future Work

- Implement more advanced NLP techniques, such as topic modeling and named entity recognition.
- Use tools like Plotly or Dash for interactive visualizations.
- Improve user interface with Streamlit for more customized analyses.