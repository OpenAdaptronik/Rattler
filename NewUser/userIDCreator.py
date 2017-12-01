def id_for_new_user(new_id, used_ids, deleted_ids):

    if len(used_ids) == 0:
        lnew_id = new_id
        used_ids.append(lnew_id)
        return lnew_id
    elif len(deleted_ids) == 0:
        lnew_id = used_ids[-1] + 1
        used_ids.append(lnew_id)
        return lnew_id
    else:
        lnew_id = deleted_ids[0]
        deleted_ids.remove(lnew_id)
        used_ids.insert(lnew_id, new_id)
        return lnew_id
