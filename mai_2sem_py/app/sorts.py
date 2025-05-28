from .models import UploadFiles

def sings(files, user):
    sings_files = []
    for i in files:
        if i.authorized_users[str(user)] == 3:
            sings_files.append(i)
    return sings_files

def non_sings(files, user):
    non_sings_files = []
    for i in files:
        if i.authorized_users[str(user)] == 2:
            non_sings_files.append(i)
    return non_sings_files

def names(files, user):
    sorted_files = []
    for i in files:
        print(i.file.file.name)
        if sorted_files:
            if i.file.file.name > sorted_files[-1].file.file.name:
                sorted_files.append(i)
            else:
                for k, j in enumerate(sorted_files):
                    if j.file.file.name < i.file.file.name:
                        sorted_files.insert(k, i)
                        break
        else:
            sorted_files.append(i)
    return sorted_files

def full_sings(files, user):
    sorted_files = []
    roles = [1, 3]
    for i in files:
        if all(x in roles for x in i.authorized_users.values()):
            sorted_files.append(i)
    return sorted_files

def uploadFiles(files, user):
    sings_files = []
    for i in files:
        if i.father_user == user:
            sings_files.append(i)
    return sings_files


def by_date(files, user):
    sorted_files = []
    for i in files:
        print(i.last_changes_date)
        if sorted_files:
            if i.last_changes_date >= sorted_files[-1].last_changes_date:
                sorted_files.append(i)
            else:
                for k, j in enumerate(sorted_files):
                    if j.last_changes_date < i.last_changes_date:
                        sorted_files.insert(k, i)
                        break
        else:
            sorted_files.append(i)
    return sorted_files[::-1]