from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import *
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier

class Constants:
    app_name = 'Buggy Code Predictor'
    input_filename = 'data.csv'
    model_filename = 'model.sav'

    models_map = {
        'naive bayes': GaussianNB,
        'knn': KNeighborsClassifier,
        'decision tree': DecisionTreeClassifier,
        'mlp': MLPClassifier
    }

    metrics_map = {
        'accuracy': accuracy_score,
        'confusion_matrix': confusion_matrix,
        'f1_score': f1_score,
        'hamming_loss': hamming_loss,
        'jaccard_score': jaccard_score,
        'precision': precision_score,
        'recall': recall_score
    }

    features_list = [
        'loc', 'cyclomatic_complexity', 'essential_complexity', 'design_complexity', 'n_operators', 'volume',
        'program_length', 'difficulty', 'intelligence', 'effort', 'halstead', 'time_estimate', 'line_count',
        'comment_lines', 'blank_lines', 'code_lines', 'unique_operators', 'unique_operands', 'tot_operators',
        'tot_operands', 'branch_count'
    ]
