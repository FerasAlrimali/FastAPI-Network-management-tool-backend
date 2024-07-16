from fastapi import HTTPException,status


def convert_filter(filter,model):
    """
    #select filters dynamically
    # raw data is "name*feras-country*libya
    """
    criteria = dict(x.split("*") for x in filter.split("-"))
    criteria_list = []
    #check every key in the dict. are there any table attributes that are the same as the dict key?
    for attr,val in criteria.items():
        try:
            _attr = getattr(model, attr)
            criteria_list.append(_attr.like(f"%{val}%"))
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"filter {attr} is not accepted")
    return criteria_list  
                
def convert_sort(sort):
    """
    # raw data "name-country"
    #we need it to be like this name,country
    split_sort = sort.split("-")
    new_sort = ','.join(split_sort)
    """
    return ",".join(sort.split('-'))


def convert_columns(columnz, model):
    """
    # raw data is = "name-sex-age"
    # we need column formatted like this --> [column(id), column(name),...] 
    # we need to seperate string using split('-')
    # we use lambda function to make code simple
    """
    try:
        return list(map(lambda x: (f"{x}: " + getattr(model,x)).label(f"{x}"),columnz.split("-")))
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"One of the columns is not accepted")