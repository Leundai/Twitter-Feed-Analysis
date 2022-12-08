import re
import json
import numpy as np


def remove_urls(text):
    # Use a regular expression to search for URLs in the input string
    # and replace them with an empty string
    return re.sub(r"https?://\S+", "", text)


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
