from datetime import datetime

from exceptions import DepositNotFound

# just example, does not persist into database
class Database:

    store = {
        "deposits": [],
    }

    def fresh():
      Database.store = {
          'deposits': []
      }

    def deposit(reference_code, amount):

      deposits = Database.store['deposits']

      deposits.append({
          'reference_code': reference_code,
          'amount': amount,
          'datetime': f"{datetime.now()}"
      })

    def retrieveAll(reference_code):

      deposits = Database.store['deposits']

      accountDeposits = [ deposit for deposit in deposits if deposit['reference_code'] == reference_code ]

      if len(accountDeposits) == 0:
          raise DepositNotFound

      return accountDeposits
        
