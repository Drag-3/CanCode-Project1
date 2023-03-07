import pandas as pd
"""
A module for processing and analyzing user input data.
Collects three sets of data from the user.
Each set must be of a homogeneous type and of three elements.
"""


def main():
    user_data = get_user_data()  # Get Data

    results = []  # Process Data
    for dataset in user_data:
        results.append(process_user_data(dataset))

    for i in range(len(results)):  # Output data
        print(f"Dataset {i + 1}: {user_data[i]}")
        print_results(results[i])
    print("Thank You!")


def get_user_data(amount: int = 3) -> list:
    """
    Function calls validate_user_data in order to get multiple sets of data
    :returns A List containing validated datasets
    """
    data_list = []
    for i in range(amount):
        print("Enter a set of data. Enter nothing to quit.")
        data_list.append(validate_user_data())
    return data_list


def numeric(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def validate_user_data() -> list:
    """
    A function that prompts the user to input a set of data,
     validates the input,
      and returns a list of the validated data.
    """
    usr_series = []
    end = False
    datatype = None
    bool_tup = ('false', 'true', 't', 'f')
    while datatype is None:  # Loop until user enters a valid dataset
        usr_input = input("Enter an element for the set. > ")
        if numeric(usr_input):
            datatype = float
            usr_series.append(float(usr_input))
        elif usr_input.lower() in bool_tup:
            datatype = bool
            usr_series.append(True if usr_input.lower() in ('true', 't') else False)
        elif usr_input == "":
            print("You need at least 3 elements to quit!")
        else:
            datatype = str
            usr_series.append(usr_input)

    while not end:
        usr_input = input("Enter an element for the set. > ")
        if numeric(usr_input) and datatype is float:
            usr_series.append(float(usr_input))
        elif usr_input.lower() in bool_tup and datatype is bool:
            usr_series.append(True if usr_input.lower() in ('true', 't') else False)
        elif usr_input == "":
            if len(usr_series) < 3:
                print("You need at least 3 elements to quit!")
            else:
                end = True
        elif datatype is str and not numeric(usr_input) and usr_input.lower() not in bool_tup[:2]:  # Only full bool
            usr_series.append(usr_input)
        else:
            print(f"Invalid datatype. dtype = {datatype}")
    return usr_series


def process_user_data(dataset: list) -> dict:
    """
    A function that takes in a list of validated user data,
     processes the data,
      and returns a dictionary containing the mean, median, mode, and total of the data.
    """
    datatype = type(dataset[0])

    results = {
        'mean': None,
        'median': None,
        'mode': None,
        'total': None
    }
    if datatype is float:  # Easiest to use pd functions
        dataset = pd.Series(dataset)
        results['mean'] = dataset.mean()
        results['median'] = dataset.median()
        mode = list(dataset.mode())
        if len(mode) != 1:
            results['mode'] = None
        else:
            results['mode'] = "".join(mode)
        results['total'] = dataset.sum()
    elif datatype is bool:  # Only mode is valid
        t_c = f_c = 0
        for elem in dataset:  # count the True count and the False count
            if elem:
                t_c += 1
            else:
                f_c += 1
        if t_c > f_c:
            results['mode'] = True
        elif f_c > t_c:
            results['mode'] = False
        else:
            results['mode'] = None
    else:  # For Strings
        sorted_dataset = sorted(dataset)
        length = len(sorted_dataset)
        # Calculate the median element(s)
        if length % 2 == 0:
            x = length // 2
            mid = [x-1, x]
        else:
            mid = [length // 2]
        res = []
        for elem in mid:
            res.append(sorted_dataset[elem])
        results['median'] = res

        # Calculate the mode. if multiple have the same amount, they are both in the mode
        counts = {}
        for elem in dataset:  # Store each element and their count in a dict
            if (counts.get(elem)) is not None:
                counts[elem] += 1
            else:
                counts[elem] = 1

        maximum = []
        for key, value in counts.items():  # Calculate the one with the most occurrences and place in a list
            if len(maximum) == 0:
                maximum.append((key, value))
            else:
                if maximum[0][1] < value:  # Clear the list as this is above all elements currently in the list
                    maximum.clear()
                    maximum.append((key, value))
                elif maximum[0][1] == value:  # Add the element to the list
                    maximum.append((key, value))
                else:
                    pass

        if len(maximum) != 1:  # If multiple elements have the same count, then the mode does not exist
            results['mode'] = None
        else:
            maxstring = ""
            for i in range(len(maximum)):  # Create a user readable string about the mode
                maxstring += str(maximum[i][0])
                if i < len(maximum) - 1:
                    maxstring += ", "
                else:
                    maxstring += f" Count = {maximum[i][1]}."
            results['mode'] = maxstring if maxstring != "" else None

        results['total'] = "".join(dataset)  # Just concatenate the strings
    return results


def print_results(result: dict):
    """
    A function that takes in the results dictionary returned by process_user_data()
     and prints the results to the console.
    """
    def _na(data):
        if data is None:
            return "N/A"
        else:
            return str(data)
    print("=" * 50)
    print(f"Mean: {_na(result['mean'])}")
    print(f"Median: {_na(result['median'])}")
    print(f"Mode: {_na(result['mode'])}")
    print(f"Total: {_na(result['total'])}")
    print("=" * 50)


if __name__ == "__main__":
    main()
