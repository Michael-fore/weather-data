import datetime 

class Ledger:
  '''
  Idk exactly where we are going to use this, but it will handle the append only csv ledger system
  that will be in the data.

  We should log errors, start runs, and end runs to the ledger, with the idea that we can
  use this for our operational needs.

  '''

  def __init__(self, file_name):
    self.startime = datetime.now()
    self.file_name = file_name
  
  def log_error(self, error):
    '''
    Log an error to the ledger
    '''
    pass

  def log_start(self):
    '''
    Log the start of a run
    '''
    pass