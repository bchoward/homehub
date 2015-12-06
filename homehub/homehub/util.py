import re


""" returns name but with capitalized letters lowercased and preceded by _"""
def dbname(s):
    return re.sub( '(?<!^)(?=[A-Z])', '_', example ).lower()

