from service.depositplan import DepositPlan
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

    depositPlanObj = DepositPlan(customerDepositPlans)

    splitAmounts[customer] = {
        'basic scenario' : depositPlanObj.get_split_amount(deposits, crossPlan=False, strategies=['default']),
        'cross-plan splitting' : depositPlanObj.get_split_amount(deposits, crossPlan=True),
        'with diminishing amount' : depositPlanObj.get_split_amount(deposits),
    }
    
    total = sum([ dep['amount'] for dep in deposits ])

    print(f'Basic split ( Customer: {customer} | Deposit:  {total} ):\n')
    pprint.pprint(splitAmounts[customer]["basic scenario"])
    print(f'\nCross-plan split ( Customer: {customer} | Deposit:  {total} ):\n')
    pprint.pprint(splitAmounts[customer]["cross-plan splitting"])
    print(f'\nCross-plan with diminishing amount split ( Customer: {customer} | Deposit:  {total} ):\n')
    pprint.pprint(splitAmounts[customer]["with diminishing amount"])

