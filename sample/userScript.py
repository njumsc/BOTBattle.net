from typing import Dict, List
import random

def getNumbers(history):
    goldenNums: List[float] = history["goldenNums"]
    userActs: Dict['name', [float, float]] = history["userActs"] 
    return [random.uniform(0, 100) for _ in range(2)]