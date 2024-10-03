import datetime 

class Ledger:
  '''
  Idk exactly where we are going to use this, but it will handle the append only csv ledger system
  that will be in the data.

  We should log errors, start runs, and end runs to the ledger, with the idea that we can
  use this for our operational needs.

  '''

  def __init__(self, product_label):
    self.startime = datetime.now()
    self.product_label = product_label
  
  def log_error(self, error):
    '''
    Log an error to the ledger
    '''
    pass

  def log_start(self, product):
    '''
    Log the start of a run
    '''
    pass

  def log_message(self, message):
    '''
    Log a message to the ledger
    '''
    pass

  def log_end(self):
    '''
    Log the end of a run
    '''
    pass