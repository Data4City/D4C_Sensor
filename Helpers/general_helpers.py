def find_occurence_in_list(list_to_check: list, condition):
    return next((obj for obj in list_to_check if condition), {})
