import ast
import math
from collections import Counter


def calculate_safety(results):
    if isinstance(results, str):
        results = ast.literal_eval(results)
    colors = [ingr[-2] for ingr in results]
    colors_count = Counter(colors)
    all_colors = sum(colors_count.values())
    safety = []
    order = ['green', 'blue', 'yellow', 'orange', 'red', 'grey']
    for col in order:
        safety.append({col: math.ceil((colors_count[col]*10)/all_colors)})
    return safety
