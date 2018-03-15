"""
Describes mock data in a dictionary to be used
to test functionality before using a live database
"""

# An array of dictionaries representing a table
_DATA = [
    {"id": "x100", "year": 2001, "make": "chevrolet", "model": "cavalier", "msrp": 10000},
    {"id": "x101", "year": 2014, "make": "chevrolet", "model": "s10", "msrp": 20000},
    {"id": "x102", "year": 2001, "make": "chevrolet", "model": "s10", "msrp": 15342},
    {"id": "x103", "year": 2014, "make": "toyota", "model": "camry", "msrp": 11432}
]

# Indexes are used in databases to quickly find data by column
# and the following dictionaries help us simulate that here.

_YEAR_INDEX = {
    "2001": [0,2],
    "2014": [1,3]
}

_MAKE_INDEX = {
    "chevrolet": [0,1,2],
    "toyota": [3]
}

_MODEL_INDEX = {
    "cavalier": [0],
    "s10": [1,2],
    "camry": [3]
}


def data_by_year(year):
    """
    Returns records that match on year
    select * from cars where year = ?
    """
    result = {}

    if year and _YEAR_INDEX.has_key(year):
        for i in _YEAR_INDEX[year]:
            result[_DATA[i]["id"]] = _DATA[i]

    return result

def data_by_make(make):
    """
    Returns records that match on make
    select * from cars where make = ?
    """
    result = {}

    if make and _MAKE_INDEX.has_key(make):
        for i in _MAKE_INDEX[make]:
            result[_DATA[i]["id"]] = _DATA[i]

    return result

def data_by_model(model):
    """
    Returns records that match on model
    select * from cars where model = ?
    """
    result = {}

    if model and _MODEL_INDEX.has_key(model):
        for i in _MODEL_INDEX[model]:
            result[_DATA[i]["id"]] = _DATA[i]

    return result

def filter_keys(year_data, make_data, model_data):
    keys = None

    # If any set of data is empty then there are no possible results
    if ((year_data is not None and len(year_data) == 0) or
        (make_data is not None and len(make_data) == 0) or
        (model_data is not None and len(model_data) == 0)):
        return keys

    if year_data:
        keys = year_data.viewkeys()

        if make_data:
            keys = keys & make_data.viewkeys()

            if model_data:
                keys = keys & model_data.viewkeys()

        elif model_data:
            keys = keys & model_data.viewkeys()

    elif make_data:
        keys = make_data.viewkeys()

        if model_data:
            keys = keys & model_data.viewkeys()

    elif model_data:
        keys = model_data.viewkeys()

    return keys

def dictionary_merge(x, y):
    z = None

    if x:
        z = x.copy()
    else:
        return y if y else None

    if y:
        z.update(y)
    else:
        return x if x else None

    return z



def get_cars_by(year, make, model):
    """
    Data is returned as an array of dictionaries filtered by the inputs.
    select * from cars where year = ? and make = ? and model = ?
    """
    result = []

    if len(year + make + model) > 0:
        car_year_data = data_by_year(year) if len(year) > 0 else None
        car_make_data = data_by_make(make.lower()) if len(make) > 0 else None
        car_model_data = data_by_model(model.lower()) if len(model) > 0 else None

        keys = filter_keys(car_year_data, car_make_data, car_model_data)

        data = dictionary_merge(car_year_data, car_make_data)
        data = dictionary_merge(data, car_model_data)

        if keys and data:
            for key in keys:
                #print "appending " + key + " into final result"
                result.append(data[key])
    else:
        # no parameters passed so return all rows
        result = _DATA

    return result