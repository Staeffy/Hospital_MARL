import collections
import csv
import pickle
import json

def show_policies(policy: dict, doc: str):
    """formatter to print the policies """

    print("---------------------------------------------------")
    print(f"#################  policy for {doc} ################")
    print("# FOR STATE --------------------------> ACTION IS #")
    print("")

    try:
        od = collections.OrderedDict(sorted(policy.items()))

    except:
        od = policy.keys()
    for keys in od:
        v = policy[keys]
        if v != ():
            if any(keys) == False:
                keys = "no one yet"
            else:
                keys = set(keys)
            print(f" {keys} treated ----------->  {v} next")
            print("")


def max_dict(d: dict):
    """Loop through dict and get max value and key"""

    max_key = max(d, key=d.get)
    max_val = d[max_key]

    # print(f"in dict {d} the max value is {max_val} with key {max_key}")
    return max_key, max_val


def store_data(data: list, name: str):
    """Appends rows to file in stats folder """

    row = data

    with open(f"stats/{name}.csv", "a") as f:
        f = csv.writer(f)
        f.writerow(row)


def save_policy(policy: dict, name: str):
    """Stores a pickl file of data in policy folder"""

    with open(f"policy/{name}.pkl", "wb") as f:
        pickle.dump(policy, f, pickle.HIGHEST_PROTOCOL)


def load_policy(name: str) -> object:
    """loads pickl file from policy folder"""

    with open(f"policy/{name}.pkl", "rb") as f:
        return pickle.load(f)


def load_json(name: str):

    with open(f'data/{name}.json') as f:
        data = json.load(f)
    return data

def transform_dict_to_tuple(data: dict) -> tuple:

    if type(data) == dict:
        new_format = []
        for item in data.keys():
            values = data[item]
            values = tuple(values)
            formatting = (item, values)
            new_format.append(formatting)

        return tuple(new_format)
    else:
        # print(f"Can't transform {data} of type {type(data)} to tuple")
        return data


def transform_tuple_to_dict(data: tuple) -> dict:

    new_format = {}
    if type(data) == tuple:
        data = dict(data)
        for keys in data.keys():
            dict_values = data[keys]
            dict_values = list(dict_values)
            new_format[keys] = dict_values

        return new_format
    else:
        return data
