"""
contains methods to get name of variables to print
"""

def get_name_to_print(str):
    if str == 'AtmPres':
        return "Pressure  [kPa]"
    elif str == 'TempC':
        return 'Temperature  [C]'
    elif str == 'RealHum':
        return 'Humidity  [?]'
    elif str == 'Cal-Cabel':
        return 'Cal???  [?]'
    else:
        return str
