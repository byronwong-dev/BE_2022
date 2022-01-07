import store.depositplan as depositPlan
import store.portfolio as portfolio
from service.portfolio import Portfolio
from fractions import Fraction
import pprint


fundsDeposit = [
  {
    'customer': 'Jackie',
    'amount': 100.50,
  },
  {
    'customer': 'Jackie',
    'amount': 1000,
  },
  {
    'customer': 'Jimmy',
    'amount': 2000,
  },
  {
    'customer': 'Jimmy',
    'amount': 1500,
  },
  {
    'customer': 'Jimmy',
    'amount': 1500,
  },
  {
    'customer': 'Samantha',
    'amount': 600,
  }
]

depositPlans = {
  'Jackie': [
    {
      'type': 'Monthly',
      'code': 'jackie-monthly',
      'portfolio': {
        'High Risk': 500.50,
        'Retirement': 200
      }
    },
    {
      'type': 'One-time',
      'code': 'jackie-onetime',
      'portfolio': {
        'High Risk': 1000,
        'Retirement': 200
      }
    }
  ],
  'Jimmy': [
    {
      'type': 'One-time',
      'code': 'jimmy-onetime',
      'portfolio': {
        'Mid Risk': 1000
      }
    },
    {
      'type': 'Monthly',
      'code': 'jimmy-monthly',
      'portfolio': {
        'Retirement': 400
      }
    },
  ],
  'Samantha': [
    {
      'type': 'Monthly',
      'code': 'samantha-monthly',
      'portfolio': {
        'Retirement': 200
      }
    },
    {
      'type': 'One-time',
      'code': 'samantha-onetime',
      'portfolio': {
        'Retirement': 500
      }
    },
  ]
}

splitAmounts = {}

for (customer, customerDepositPlans) in depositPlans.items():

    deposits = [ deposit for deposit in fundsDeposit if deposit['customer'] == customer ]

    splitAmounts[customer] = {
        'basic scenario' : Portfolio.get_split_amount(customerDepositPlans, deposits, crossPlan=False, strategies=['default']),
        'cross-plan splitting' : Portfolio.get_split_amount(customerDepositPlans, deposits, crossPlan=True),
        'with diminishing amount' : Portfolio.get_split_amount(customerDepositPlans, deposits),
    }
    
    total = sum([ dep['amount'] for dep in deposits ])

    print(f'Customer: {customer} | Deposit: {total}\n')
    print(f'Basic split:\n')
    pprint.pprint(splitAmounts[customer]["basic scenario"])
    print(f'\nCross-plan split:\n')
    pprint.pprint(splitAmounts[customer]["cross-plan splitting"])
    print(f'\nDeposits: {total} \n')
    print(f'\nCross-plan with diminishing amount split:\n')
    pprint.pprint(splitAmounts[customer]["with diminishing amount"])
# json.dumps(splitAmounts, indent=2)
