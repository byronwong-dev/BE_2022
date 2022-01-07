from fractions import Fraction

def is_diminishing_ratio(numerator, denominator = 1):

    if numerator == 0 or numerator is None:
        return False

    if type(numerator) == Fraction:
        return is_diminishing_ratio(numerator.numerator, numerator.denominator)
    
    if denominator / numerator > 100:
        return True
    
    return False

def get_diminishing_amounts(amounts):

    maxAmount = max(amounts)

    diminishingAmounts = [ amount for amount in amounts if is_diminishing_ratio(amount, maxAmount) ]

    if len(diminishingAmounts) == 0:
        return None

    return diminishingAmounts
