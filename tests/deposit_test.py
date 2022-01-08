from service.depositplan import DepositPlan
from fractions import Fraction

def test_can_obtain_split_ratio_for_deposit_plan():

  depositPlans = [
    {
      'type': 'One-time',
      'code': '1-onetime',
      'portfolio': {
        'High Risk': 1000,
        'Retirement': 500
      }
    },
    {
      'type': 'Monthly',
      'code': '1-monthly',
      'portfolio': {
        'Retirement': 200
      }
    }
  ]

  depositPlanObj = DepositPlan(depositPlans)
  
  depositPlanObj.append_ratio(crossPlan = True)
  
  assert list(depositPlanObj.depositPlans[0]['ratio'].keys()) == ['High Risk', 'Retirement']
  assert float(Fraction(10, 17)) == float(Fraction(depositPlanObj.depositPlans[0]['ratio']['High Risk']))
  assert float(Fraction(5,17)) ==  float(Fraction(depositPlanObj.depositPlans[0]['ratio']['Retirement']))

  assert float(Fraction(2, 17)) == float(Fraction(depositPlanObj.depositPlans[1]['ratio']['Retirement']))

  depositPlanObj.append_ratio(crossPlan = False)
  assert list(depositPlanObj.depositPlans[0]['ratio'].keys()) == ['High Risk', 'Retirement']
  assert float(Fraction(2,3)) == float(depositPlanObj.depositPlans[0]['ratio']['High Risk'])
  assert float(Fraction(1,3)) ==  float(depositPlanObj.depositPlans[0]['ratio']['Retirement'])

  assert 1 == depositPlanObj.depositPlans[1]['ratio']['Retirement']

def test_can_obtain_split_amount_given_ratio():
  depositPlans = [
    {
      'type': 'One-time',
      'code': '1-onetime',
      'portfolio': {
        'High Risk': 1000,
        'Retirement': 500
      }
    },
    {
      'type': 'Monthly',
      'code': '1-monthly',
      'portfolio': {
        'Retirement': 200,
        'Simple Life': 200,
        'Adventure': 200
      }
    }
  ]

  deposits = [
    {
      'amount': 1500,
    },
  ]

  depositPlanObj = DepositPlan(depositPlans)

  splitAmount = depositPlanObj.get_split_amount(deposits, crossPlan = False)

  assert 1000 == splitAmount[0]['split']['High Risk']
  assert 500 == splitAmount[0]['split']['Retirement']
  assert 0 == splitAmount[1]['split']['Retirement']
  assert 0 == splitAmount[1]['split']['Simple Life']
  assert 0 == splitAmount[1]['split']['Adventure']

  splitAmount = depositPlanObj.get_split_amount(deposits, crossPlan = True)

  assert 714.286 == splitAmount[0]['split']['High Risk']
  assert 357.143 == splitAmount[0]['split']['Retirement']
  assert 142.857 == splitAmount[1]['split']['Retirement']
  assert 142.857 == splitAmount[1]['split']['Simple Life']
  assert 142.857 == splitAmount[1]['split']['Adventure']

def test_amount_overflow_give_one_time_first():

  depositPlans = [
    {
      'type': 'Monthly',
      'code': '1-monthly',
      'portfolio': {
        'High Risk': 500.50,
        'Retirement': 200,
      }
    },
    {
      'type': 'One-time',
      'code': '1-onetime',
      'portfolio': {
        'High Risk': 1000,
        'Retirement': 200
      }
    }
  ]

  deposits = [
    {
      'amount': 1100.50,
    },
  ]

  depositsOnlyForOneTime = [
    {
      'amount': 1200,
    },
  ]

  depositPlanObj = DepositPlan(depositPlans)

  splitAmount = depositPlanObj.get_split_amount(deposits, crossPlan = False, strategies=['default'])

  assert 917.083 == splitAmount[0]['split']['High Risk']
  assert 183.417 == splitAmount[0]['split']['Retirement']
  assert 0 == splitAmount[1]['split']['Retirement']
  assert 0 == splitAmount[1]['split']['Retirement']


  splitAmount = depositPlanObj.get_split_amount(depositsOnlyForOneTime, crossPlan = False, strategies=['default'])
  assert 1000 == splitAmount[0]['split']['High Risk']
  assert 200 == splitAmount[0]['split']['Retirement']
  assert 0 == splitAmount[1]['split']['High Risk']
  assert 0 == splitAmount[1]['split']['Retirement']


def test_amount_overflow_multiple_times_give_one_time_first():

  depositPlans = [
    {
      'type': 'Monthly',
      'code': '1-monthly',
      'portfolio': {
        'High Risk': 400,
      }
    },
    {
      'type': 'One-time',
      'code': '1-onetime',
      'portfolio': {
        'Retirement': 1000,
      }
    }
  ]

  deposits = [
    {
      'amount': 5000,
    },
  ]

  depositPlanObj = DepositPlan(depositPlans)

  splitAmount = depositPlanObj.get_split_amount(deposits, crossPlan = False, strategies=['default'])

  assert 3571.429 == splitAmount[0]['split']['Retirement']
  assert 1428.571 == splitAmount[1]['split']['High Risk']


def test_can_obtain_split_decimal_amount_given_ratio():
  depositPlans = [
    {
      'type': 'One-time',
      'code': '1-onetime',
      'portfolio': {
        'High Risk': 1000.50,
        'Retirement': 499.50
      }
    },
    {
      'type': 'Monthly',
      'code': '1-monthly',
      'portfolio': {
        'Retirement': 200
      }
    }
  ]

  deposits = [
    {
      'amount': 1000,
    }
  ]

  multipleDeposits = [
    {
      'amount': 1000.50,
    },
    {
      'amount': 225
    }
  ]

  depositPlanObj = DepositPlan(depositPlans)
  
  splittedDepositPlans = depositPlanObj.get_split_amount(deposits, crossPlan=False)

  assert 667 == splittedDepositPlans[0]['split']['High Risk']
  assert 333 == splittedDepositPlans[0]['split']['Retirement']

  multipleDepositSplitAmount = depositPlanObj.get_split_amount(multipleDeposits, crossPlan=False)

  assert 817.409 == multipleDepositSplitAmount[0]['split']['High Risk']
  assert 408.091 == multipleDepositSplitAmount[0]['split']['Retirement']

  splittedDepositPlans = depositPlanObj.get_split_amount(deposits, crossPlan=True)

  assert 588.529 == splittedDepositPlans[0]['split']['High Risk']
  assert 293.824 == splittedDepositPlans[0]['split']['Retirement']
  assert 117.647 == splittedDepositPlans[1]['split']['Retirement']

  multipleDepositSplitAmount = depositPlanObj.get_split_amount(multipleDeposits, crossPlan=True)

  assert 721.243 == multipleDepositSplitAmount[0]['split']['High Risk']
  assert 360.081 == multipleDepositSplitAmount[0]['split']['Retirement']
  assert 144.176 == multipleDepositSplitAmount[1]['split']['Retirement']


def test_significant_uneven_ratio():
  depositPlans = [
    {
      'type': 'One-time',
      'code': '1-onetime',
      'portfolio': {
        'High Risk': 10000,
        'Retirement': 2.50
      }
    },
  ]

  deposits = [
    {
      'amount': 1000,
    }
  ]

  depositPlanObj = DepositPlan(depositPlans)
  
  splittedDepositPlans = depositPlanObj.get_split_amount(deposits, crossPlan=False, strategies=['diminishing-first'])
  
  assert 997.50 == splittedDepositPlans[0]['split']['High Risk']
  assert 2.50 == splittedDepositPlans[0]['split']['Retirement']

def test_significant_uneven_ratio_multi_profile():
  depositPlanMultiProfile = {
      'type': 'Monthly',
      'code': '1-monthly',
      'portfolio': {
        'High Risk': 5000,
        'Mid Risk': 5000,
        'Retirement': 2.50
      }
  }

  deposits = [
    {
      'amount': 2000,
    }
  ]

  depositPlanObj = DepositPlan(depositPlanMultiProfile)

  splittedDepositPlans = depositPlanObj.get_split_amount(deposits, crossPlan=False, strategies=['diminishing-first'])

  assert 998.75 == splittedDepositPlans[0]['split']['High Risk']
  assert 998.75 == splittedDepositPlans[0]['split']['Mid Risk']
  assert 2.50 == splittedDepositPlans[0]['split']['Retirement']


def test_significant_uneven_ratio_multi_profile_decimals():
  depositPlanMultiProfile = {
      'type': 'Monthly',
      'code': '1-monthly',
      'portfolio': {
        'High Risk': 5000,
        'Mid Risk': 3050.50,
        'Retirement': 2.50
      }
  }

  deposits = [
    {
      'amount': 2000,
    }
  ]

  depositPlanObj = DepositPlan(depositPlanMultiProfile)

  splittedDepositPlans = depositPlanObj.get_split_amount(deposits, crossPlan=False, strategies=['diminishing-first'])

  assert 1240.606 == splittedDepositPlans[0]['split']['High Risk']
  assert 756.894 == splittedDepositPlans[0]['split']['Mid Risk']
  assert 2.50 == splittedDepositPlans[0]['split']['Retirement']
