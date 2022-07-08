
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

def get_names(computers):
    names = []
    for c in computers:
        if c.name not in names:
            names.append(c.name)
    return names

def get_serials(computers):
    serials = []
    for c in computers:
        if c.serial not in serials:
            serials.append(c.serial)
    return serials

def get_activities(computers):
    acts = []
    for c in computers:
        if c.is_active not in acts:
            acts.append(c.is_active)
    return acts

def get_ten(computers, index):
    ten = []
    index = index * 10
    #if page can be completely filled
    if len(computers) >= (index):
        index = index - 10
        for i in range(0, 10):
            ten.append(computers[index + i])
        
    #if parital page
    elif len(computers) < (index) and len(computers) > (index - 10):
        index = index - 10
        for i in range(0, (len(computers) % 10)):
            ten.append(computers[index + i])

    #if page isnt filled
    elif len(computers) < (index - 10):
        return get_ten(computers, int(index /10) - 1)
        
    return ten
        



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

def sort_admins(all_users, current_user):
    admins = []
    for u in all_users:
        if (u.is_admin) and (u.email is not current_user.email):
            admins.append(u)

    users = []
    for u in all_users:
        if not(u.is_admin):
            users.append(u)
    return admins, users


