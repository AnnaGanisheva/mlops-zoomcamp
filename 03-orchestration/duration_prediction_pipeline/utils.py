import pickle
import os


def save_pickle(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f_out:
        pickle.dump(obj, f_out)


def load_pickle(path):
    with open(path, "rb") as f_in:
        return pickle.load(f_in)