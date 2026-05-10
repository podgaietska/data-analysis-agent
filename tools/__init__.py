"""Tool registry — exposes all_tools list."""

from tools.summary import preload_datasets, get_dataset_summaries
from tools.dataframe_ops import call_dataframe_method
from tools.classification import evaluate_classification_dataset
from tools.regression import evaluate_regression_dataset

all_tools = [
    preload_datasets,
    get_dataset_summaries,
    call_dataframe_method,
    evaluate_classification_dataset,
    evaluate_regression_dataset,
]
