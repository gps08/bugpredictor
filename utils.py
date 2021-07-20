from models import Features
from consts import Constants
import numpy as np
from radon import metrics, raw
from radon.metrics import mi_parameters
import ast
import os

# this method assumes that code given is in python language
def get_features(code: str):
    basics = raw.analyze(code)
    hs = metrics.h_visit(code).total
    complexity = mi_parameters(code)[1]
    tree = ast.parse(code)
    l_dash = 0 if hs.h1*hs.N1 == 0 else hs.h2/(hs.h1*hs.N1)
    return Features(
        loc=basics.loc,
        cyclomatic_complexity=complexity,
        essential_complexity=complexity,
        design_complexity=complexity,
        n_operators=hs.N1+hs.N2,
        volume=hs.volume,
        program_length=hs.length,
        difficulty=hs.difficulty,
        intelligence=hs.volume*l_dash,
        effort=hs.effort,
        halstead=hs.bugs,
        time_estimate=hs.time,
        line_count=basics.loc,
        comment_lines=basics.comments,
        blank_lines=basics.blank,
        code_lines=basics.lloc,
        unique_operators=hs.h1,
        unique_operands=hs.h2,
        tot_operators=hs.N1,
        tot_operands=hs.N2,
        branch_count=sum([1 if isinstance(x, ast.If) else 0 for x in ast.walk(tree)])
    )

def load_data(features, sep=','):
    cols = [Constants.features_list.index(f) for f in features]
    x = np.loadtxt(Constants.input_filename, delimiter=sep, skiprows=1, usecols=cols)
    y = np.loadtxt(Constants.input_filename, delimiter=sep, skiprows=1)[:, -1]
    return x, y

def get_repo_name(url):
    return url.split('/')[-1].replace('.git', '')

def load_repo(url):
    repo_name = get_repo_name(url)
    if not os.path.isdir(repo_name):
        os.system(f'git clone {url}')
    paths = []
    for r, _, f in os.walk(repo_name):
        py_files = [os.path.join(r, file) for file in f if file.endswith(".py")]
        if len(py_files) > 0:
            paths += py_files
    return paths
