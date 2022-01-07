from re import split
from exceptions import ParameterFormatException, InvalidDepositPlanException
from fractions import Fraction

from helpers import ratio

class Portfolio:

  def append_portfolio_ratio(depositPlans, crossPlan = False):
    if type(depositPlans) is not list and type(depositPlans) is dict:
      depositPlans = [depositPlans]

    ratios = []

    totalAmount = sum([ amount for plan in depositPlans for (portfolio, amount) in plan['portfolio'].items()  ])

    for depositPlan in depositPlans:

      totalPlanAmount = sum([ amount for (portfolio, amount) in depositPlan['portfolio'].items()])
      
      if not crossPlan:
        ratios.append({
          **depositPlan,
          'ratio': { portfolio: Fraction(amt / totalPlanAmount) for (portfolio, amt) in depositPlan['portfolio'].items() }
          })
      else:
        ratios.append({
          **depositPlan,
          'ratio': { portfolio: Fraction(amt / totalAmount) for (portfolio, amt) in depositPlan['portfolio'].items() }
          })

    return ratios


  def get_split_amount(depositPlans, deposits, crossPlan = False, strategies = ['default']):
    """ get split amount

    Args:
        depositPlans list: 
        deposits dict:
        crossPlan (boolean, optional): if True, will calculate ratio via aggregate across plans
        strategies (list, optional): apply strategy in splitting the amount. Available: 'diminishing-first' (where in the case there is a diminishing amount, allocate that amount first, currently cross deposit plan)

    Raises:
        ParameterFormatException: [description]
        InvalidDepositPlanException: [description]

    Returns:
        [type]: [description]
    """

    numDepositPlans = len(depositPlans)

    ratioedDepositPlans = Portfolio.append_portfolio_ratio(depositPlans, crossPlan)

    totalDeposits = sum([deposit['amount'] for deposit in deposits])

    # default strategy
    if 'default' in strategies and crossPlan is False and numDepositPlans == 2:
      return Portfolio._spit_default(ratioedDepositPlans, totalDeposits, crossPlan)

    
    portfolioAmounts = [ amount for depositPlan in ratioedDepositPlans for (portfolio, amount) in depositPlan['portfolio'].items()]

    diminishingAmounts = ratio.get_diminishing_amounts(portfolioAmounts)

    # diminish amount exists
    if 'diminishing-first' in strategies and diminishingAmounts:
      return Portfolio._split_following_diminish_first(ratioedDepositPlans, diminishingAmounts, totalDeposits)
    
    # following ratio fallback
    for depositPlan in ratioedDepositPlans:  
      splittedAmount = Portfolio._get_split_amount(depositPlan, totalDeposits)
      depositPlan['split'] = splittedAmount

    return ratioedDepositPlans


  def _get_split_amount(depositPlan, totalAmount) -> dict:

    if totalAmount == 0:
      return { portfolio: 0 for (portfolio, ratio) in depositPlan['ratio'].items() }

    return { portfolio: round(float(ratio * totalAmount),3) for (portfolio, ratio) in depositPlan['ratio'].items() }


  def _split_following_diminish_first(depositPlans, diminishingAmounts, totalAmount):

    # get the deductable amount after diminishing amount 
    totalAmount -= sum(diminishingAmounts)

    # readjust the ratio of non-diminishing amount portfolio based on its own pool
    adjustedDepositPlans = Portfolio._adjust_ratio_for_non_diminishing_portfolio_amount(depositPlans, diminishingAmounts)

    # split the amount
    for depositPlan in adjustedDepositPlans:
      for (depositPlanPortfolio, amount) in depositPlan['portfolio'].items():

        if 'split' not in depositPlan:
          depositPlan['split'] = {}
        
        if amount not in diminishingAmounts:
          
          depositPlan['split'][depositPlanPortfolio] = round(float(totalAmount * depositPlan['ratio'][depositPlanPortfolio]),3)
        else:
          depositPlan['split'][depositPlanPortfolio] = amount

    return adjustedDepositPlans


  def _adjust_ratio_for_non_diminishing_portfolio_amount(depositPlans, diminishingAmounts):

    totalAmount = 0
    amountToAdjust = {}

    for depositPlan in depositPlans:
      for (portfolio, amount) in depositPlan['portfolio'].items():
        if amount not in diminishingAmounts:
          totalAmount += amount
          amountToAdjust[f'{depositPlan["code"]}_{portfolio}'] = amount

    adjustedDepositPlan = [d for d in depositPlans]

    for depositPlan in adjustedDepositPlan:
      for (portfolio, amount) in depositPlan['portfolio'].items():
        if f'{depositPlan["code"]}_{portfolio}' in amountToAdjust:
          depositPlan['ratio'][portfolio] = Fraction(amount / totalAmount)          

    return adjustedDepositPlan


  def _sorted_deposit_plans(depositPlans):

      sortOrder = {
        'One-time': 1,
        'Monthly': 2
      }

      depositPlans.sort(key=lambda x: sortOrder[x['type']])

  def _spit_default(depositPlans, totalDeposits, crossPlan=False):
    """Default strategy to split

    Args:
        depositPlans ([type]): [description]
        totalDeposits ([type]): [description]
        crossPlan (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """

    Portfolio._sorted_deposit_plans(depositPlans)
    totalExpectedAmount = Portfolio._get_all_plans_expected_amount(depositPlans)

    # if more than total, we assign by ratio
    if totalDeposits >= totalExpectedAmount:
      crossPlan = True
      depositPlans = Portfolio.append_portfolio_ratio(depositPlans, crossPlan)
    
    for depositPlan in depositPlans:

      currentPlanExpectedAmount = Portfolio._get_current_plan_expected_amount(depositPlan)

      splittedAmount = Portfolio._get_split_amount(depositPlan, totalDeposits)
      depositPlan['split'] = splittedAmount
      if not crossPlan:
        totalDeposits -= sum([value for p, value in splittedAmount.items()])

    return depositPlans
    

  def _get_current_plan_expected_amount(depositPlan):
    return sum([amount for (currentPlanName, amount) in depositPlan['portfolio'].items()])
    
  def _get_all_plans_expected_amount(depositPlans):
    return sum([amount for depositPlan in depositPlans for (currentPlanName, amount) in depositPlan['portfolio'].items()])