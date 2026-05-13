def row_to_dict(row):
    return dict(row) if row is not None else None

def rows_to_list(rows):
    return [dict(row) for row in rows]
