# This task is evaluated by LLM-as-judge only; no rule-based checkpoints by design.
import re
import logging
from typing import List

from scoring import Result, Checkpoint
from common import grader


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    return result
