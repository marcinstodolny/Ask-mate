import data_manager


def sort_list(sort_by="submission_time", order_direction="DESC", limit=""):
    return data_manager.get_sorted_data(sort_by, order_direction, limit)
