"""
****************************
* Type checking facilities *
****************************
"""
is_null            = lambda x : x is None
is_of_type         = lambda x, y : isinstance(x, y)
is_string          = lambda x : is_of_type(x, str)
is_type            = lambda x : is_of_type(x, type)
is_value           = lambda x : is_of_type(x, Value)
is_int             = lambda x : is_of_type(x, int) and not is_of_type(x, bool)

is_collectible             = lambda x : is_of_type(x, list) or is_of_type(x, tuple)
is_dict                    = lambda x : is_of_type(x, dict)
is_collectible_conditional = lambda x, cond : False not in (map(lambda y : cond(y), x))
is_collectible_of_type     = lambda x, tp : is_collectible_conditional(x, lambda y : is_of_type(y, tp))

is_string_coll          = lambda x : is_collectible_of_type(x, str)
is_type_coll            = lambda x : is_collectible_of_type(x, type)
is_value_coll           = lambda x : is_collectible_of_type(x, Value)




def is_dict_conditional(dic, cond):
    if not is_dict(dic):
        return False

    for k in dic.keys():
        v = dic[k]
        if not cond(k, v):
            return False

    return True


def is_dict_of_types(keyT, valueT, dic):
    cond = lambda k, v : is_of_type(k, keyT) and is_of_type(v, valueT)
    return is_dict_conditional(dic, cond)


is_str_type_dict        = lambda x : is_dict_of_types(str, type, x)

is_value_dict           = lambda x : is_dict_of_types(str, Value, x)





def is_collectible_of_specified_types(coll, types):
    n = len(coll)

    for i in range(0, n):
        currEl = coll[i]
        currType = types[i]

        if not is_null(currEl) and not is_of_type(currEl, currType):
            return False

    return True



"""
***********************
* Deepcopy facilities *
***********************
"""
deepcopy_coll         = lambda x, y : y(map(lambda y : deepcopy(y), x))
deepcopy_list         = lambda x : deepcopy_coll(x, list)
deepcopy_tuple        = lambda x : deepcopy_coll(x, tuple)


def deepcopy_dict(x):
    d = {}
    for i in x.keys():
        kd = deepcopy(i)
        d[kd] = deepcopy(x[i])

    return d




"""
*********************************
* Text justification facilities *
*********************************
"""

justify_single = lambda x, y : ("%%-%ds" % (y,)) % (x,)

def justify_multiple(row, cellTextWidths):
    nEls = len(cellTextWidths)
    for i in range(0, nEls):
        row[i] = justify_single(row[i], cellTextWidths[i])



#########################################
#########################################
#########################################
#########################################


get_value_raw_values    = lambda x : tuple(map(lambda y : y.getRawValue(), x))




#########################################
#########################################
#########################################
#########################################

"""
intFunct(obj, sel, isSingle=True, isStart=None)
strFunct(obj, sel, isSingle=True, isStart=None)
"""


def genericGetItem(obj, sel, noneFunct, intFunct, stringFunct, solveSlice):
    if is_of_type(sel, slice):
        return genericGetSlice(obj, sel, noneFunct, intFunct, stringFunct, solveSlice)

    elif is_int(sel):
        return intFunct(obj, sel, isSingle=True)

    elif stringFunct is not None and is_string(sel):
        return stringFunct(obj, sel, isSingle=True)

    else:
        raise IndexError("Error: unexpected value for getitem: \"%s\"" % (str(sel),))


def genericGetSlice(obj, sel, noneFunct, intFunct, stringFunct, solveSlice):
    start = sel.start
    end = sel.stop

    if start is None:
        start = noneFunct(obj, sel, isSingle=False, isStart=True)

    elif isInt(start):
        start = intFunct(obj, sel, isSingle=False, isStart=True)

    elif stringFunct is not None and isString(start):
        start = stringFunct(obj, sel, isSingle=False, isStart=True)

    if end is None:
        end = noneFunct(obj, sel, isSingle=False, isStart=False)

    elif isInt(end):
        end = intFunct(obj, sel, isSingle=False, isStart=False)

    elif stringFunct is not None and isString(end):
        end = stringFunct(obj, sel, isSingle=False, isStart=False)

    return solveSlice(obj, start, end)