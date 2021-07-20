from pydantic import BaseModel

# input model for a training request to the system
class TrainIn(BaseModel):
    model_name: str
    metrics: list[str]
    feature_cols: list[str]
    extra_params: dict

# model for query to the prediction model
class QueryIn(BaseModel):
    snippets: list[str]

# feedback input model
class FeedbackIn(BaseModel):
    code: str
    is_buggy: bool

# feature set model for internal use
class Features(BaseModel):
    loc: float
    cyclomatic_complexity: float
    essential_complexity: float
    design_complexity: float
    n_operators: float
    volume: float
    program_length: float
    difficulty: float
    intelligence: float
    effort: float
    halstead: float
    time_estimate: float
    line_count: float
    comment_lines: float
    blank_lines: float
    code_lines: float
    unique_operators: float
    unique_operands: float
    tot_operators: float
    tot_operands: float
    branch_count: float

    def as_list(self, features_list):
        ret = []
        for f in features_list:
            ret.append(self.__dict__[f])
        return ret
