import pandas as pd
import itertools
import numpy as np
import ast

def generate_ngram_composition(sequence, n):
    """
    Generate n-gram composition for a given sequence.
    
    Args:
        sequence (str): The protein sequence.
        n (int): The length of the n-gram.
        
    Returns:
        ngram_features (list): A list of n-gram composition features.
    """
    # Define the set of amino acids considered in the protein sequences.
    amino_acids = 'ACDEFGHIKLMNPQRSTVWY'

    # Generate all possible n-grams from the set of amino acids.
    ngrams = [''.join(ngram) for ngram in itertools.product(amino_acids, repeat=n)]

    # Calculate the composition of each n-gram in the sequence.
    ngram_features = [round(sequence.count(ngram) / len(sequence), 3) for ngram in ngrams]

    return ngram_features

def generate_ngram_occurences(sequence, n):
    """
    Generate n-gram occurrences for a given sequence.
    
    Args:
        sequence (str): The protein sequence.
        n (int): The length of the n-gram.
        
    Returns:
        ngram_features (list): A list of n-gram occurrence features.
    """
    # Define the set of amino acids considered in the protein sequences
    amino_acids = 'ACDEFGHIKLMNPQRSTVWY'

    # Generate all possible n-grams from the set of amino acids.
    ngrams = [''.join(ngram) for ngram in itertools.product(amino_acids, repeat=n)]

    # Count occurrences of each n-gram in the given sequence.
    ngram_features = [sequence.count(ngram)  for ngram in ngrams]

    return ngram_features


def generate_features(df, features):
    """
    Generate monogram and bigram features for each protein sequence in a DataFrame.
    
    Args:
        df (DataFrame): The input DataFrame containing protein sequences.
        
    Returns:
        df (DataFrame): The DataFrame with added feature columns.
    """
    for feat_name in features:
        if feat_name == 'MonogramComp':
            # Generate monogram composition features
            df['MonogramComp'] = df['Sequence'].apply(lambda seq: generate_ngram_composition(seq, 1))
        elif feat_name == 'BigramComp':
            # Generate bigram composition features
            df['BigramComp'] = df['Sequence'].apply(lambda seq: generate_ngram_composition(seq, 2))
        elif feat_name == 'TrigramComp':
            # Generate trigram composition features
            df['TrigramComp'] = df['Sequence'].apply(lambda seq: generate_ngram_composition(seq, 3))
        elif feat_name == 'MonogramOccur':
            # Generate monogram occurrence features
            df['MonogramOccur'] = df['Sequence'].apply(lambda seq: generate_ngram_occurences(seq, 1))
        else:
            # Generate bigram occurrence features
            df['BigramOccur'] = df['Sequence'].apply(lambda seq: generate_ngram_occurences(seq, 2))
    
    return df

def concatenate_columns(row, columns):
    """
    Concatenate lists from specified columns of a DataFrame row into a single list.
    
    Args:
        row (Series): A pandas Series representing a row of a DataFrame.
        columns (list): A list of column names containing lists to concatenate.
        
    Returns:
        concatenated_list (list): A single list containing the concatenated elements from specified columns.
    """
    concatenated_list = []
    for col in columns:
        concatenated_list += row[col]
    return concatenated_list

def process_features(data_path, features):
  """
    Process features from a given dataset and a specified feature type.
    
    Args:
        data_path (str): Path to the dataset CSV file.
        feature (str): The type of feature to process (e.g., 'MonogramComp', 'BigramComp').
        
    Returns:
        tuple: A tuple containing the feature array, labels, and sequences.
    """
  # Read dataset and shuffle
  data_df = pd.read_csv(data_path)
  data_df = data_df.sample(frac = 1)

  #generating features
  feature_df = generate_features(data_df, features)

  # Select specified features and labels
  feature_df['Features'] = feature_df.apply(lambda row: concatenate_columns(row, features), axis=1)
  feature_df = feature_df[['Features', 'Label','Sequence']].reset_index(drop=True)

  # Prepare data for training/ testing set
  X_data = feature_df['Features'].tolist()
  label = feature_df['Label'].to_numpy()
  sequences = feature_df['Sequence'].tolist()

  return np.array(X_data), label, sequences
