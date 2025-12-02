def _parse_column_def(column_def):
    if ':' in column_def:
        name, col_type = column_def.split(':', 1)
        return name.strip(), col_type.strip().lower()
    return column_def.strip(), 'str'

def _parse_where_clause(where_str):
    if not where_str:
        return {}
    
    conditions = {}
    if 'AND' in where_str:
        parts = where_str.split('AND')
    else:
        parts = [where_str]
    
    for part in parts:
        part = part.strip()
        if '=' in part:
            key, value = part.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            if (value.startswith("'") and value.endswith("'")) or \
               (value.startswith('"') and value.endswith('"')):
                value = value[1:-1]
            
            conditions[key] = value
    
    return conditions

def _parse_set_clause(set_str):
    updates = {}
    parts = set_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '=' in part:
            key, value = part.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            if (value.startswith("'") and value.endswith("'")) or \
               (value.startswith('"') and value.endswith('"')):
                value = value[1:-1]
            
            updates[key] = value
    
    return updates