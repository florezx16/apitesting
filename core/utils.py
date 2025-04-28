from django.db.models import Q

def PrepareFilters(data,filters_dict):
    query_filters = Q()
    for k,v in data.items():
        if v:#Check if the value is available
            filter_type = filters_dict.get(k)
            if isinstance(filter_type,list):#Check if filter_type has relationship
                field_name, filter_type = filter_type[0], filter_type[1] #Assign the values
            else:
                field_name, filter_type = k, filter_type
            query_condition = f'{field_name}__{filter_type}' #Prepare query conditions based on filter_type
            query_filters &= Q(**{query_condition:v}) #Send as argument the query condition(dict)
    query_filters &= Q(status = 1)
    return query_filters