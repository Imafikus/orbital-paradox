import datetime

def check_positive_int(value):
    """
    Checks if provided value is positive integer.

    Returns True or False
    """
    check = True
    try:
        int(value)
    except ValueError:
        check = False
        return check

    if int(value) < 0:
        check = False
        return check
    
    return check

def check_positive_float(value):
    """
    Checks if provided value is positive float.

    Returns True or False
    """
    check = True
    try:
        float(value)
    except ValueError:
        check = False
        return check
    if float(value) < 0:
        check = False
        return check
    
    return check

def check_datetime(value):
    """
    Checks if provided value is a valid date in DD-MM-YYYY format.

    Returns True or False
    """

    check = True
    #check if all three values were given
    try:
        day, month, year = value.split('-')
    except ValueError:
        check = False
        return check
    #try if they are valid values for DD-MM-YYYY format
    try :
        #datetime.datetime.strptime(value, "%d-%m-%Y")
        datetime.datetime.strptime(value, "%Y-%m-%d")
    
    except ValueError:
        check = False
        return check

    return check

def check_for_letters(name):
    """
    Checks if provided name has at least 1 letter.

    Returns True or False
    """
    check = True
    
    if not isinstance(name, str) or name.isdigit() or name == "":
        check = False
    
    return check

def check_email(email):
    """
    Checks if provided value is a valid email.

    Returns True or False
    """
    check = True

    if "@" not in email:
        check = False
        return check

    before_at, after_at = email.split("@")
    
    if "." not in after_at:
        check = False
        return check

    if len(before_at) == 0 or len(after_at) == 0:
       check = False
       return check
    
    before_dot, after_dot = after_at.split(".")
    
    if len(before_dot) == 0 or len(after_dot) == 0:
       check = False
       return check
    
    return check


