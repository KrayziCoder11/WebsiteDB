
def get_locations(computers):
    locations = []
    for c in computers:
        if c.location not in locations:
            locations.append(c.location)
    return locations

def get_user_names(computers):
    names = []
    for c in computers:
        if c.user_name not in names:
            names.append(c.user_name)
    return names

def get_models(computers):
    models = []
    for c in computers:
        if c.model not in models:
            models.append(c.model)
    return models


def selectionSort(computers):
    size = len(computers)
    for s in range(size):
        min_idx = s
         
        for i in range(s + 1, size):
             
            # For sorting in descending order
            # for minimum element in each loop
            if computers[i].name < computers[min_idx].name:
                min_idx = i
 
        # Arranging min at the correct position
        (computers[s], computers[min_idx]) = (computers[min_idx], computers[s])
    return computers