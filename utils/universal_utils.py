def calculate_bundles(weight):
    if weight <= 100:
        bundles = 1
    else:
        bundles = (weight - 100) // 100 + 1

    return bundles


def add_bundles(weight, num_bundles):
    bundles = calculate_bundles(weight)
    total_weight = weight + num_bundles * bundles
    return total_weight


def subtract_bundles(weight, num_bundles):
    bundles = calculate_bundles(weight)
    total_weight = weight - num_bundles * bundles
    return total_weight