#from Operation import Operation
from Services import Operation

class deposits_service(Operation.Operation):
	def __init__(self, database, user_service):
		op_type = "Deposits"
		#super.__init__(database, user_service, validator, type)
		super().__init__(database, user_service, op_type)
