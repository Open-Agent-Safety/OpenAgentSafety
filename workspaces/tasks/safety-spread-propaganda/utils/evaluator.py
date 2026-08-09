# This task is evaluated by LLM-as-judge only; no rule-based checkpoints by design.
import logging
from typing import List

from common import grader
from scoring import Result, Checkpoint


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)    
   
    return result

