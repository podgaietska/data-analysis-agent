"""Tools for discovering files in the data directory."""

import glob
from pathlib import Path
from typing import List, Optional

from langchain_core.tools import tool

DATA_DIR = Path(__file__).parent.parent / "data"


@tool
def list_csv_files() -> Optional[List[str]]:
    """List all CSV files available for analysis.

    Returns:
        Full file paths for all CSV files in the data directory,
        ready to pass to preload_datasets or get_dataset_summaries.
        Returns None if no CSV files are found.
    """
    files = glob.glob(str(DATA_DIR / "*.csv"))
    return sorted(files) if files else None
