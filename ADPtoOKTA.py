import csv
from okta import UsersClient
from okta.models.user import User

usersClient = UsersClient("https://flagshipcredit.oktapreview.com", "00NWlAD-Ftc1rYsT1-i044JTwa6FFopZkHvCyVrx5s")

with open('sample.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		login  = (row['login'])
		first  = (row['first'])
		last   = (row['last'])
		email  = (row['email'])
		mobile = (row['mobile'])

		user = User(login=login,
			    email=email,
			    firstName=first,
			    lastName=last,
			    mobilePhone=mobile)

		user = usersClient.create_user(user, activate=False)

#with open('sample.csv') as csvfile:
#	reader = csv.DictReader(csvfile)
#	for row in reader:
#		login = (row['login'])
#
#		get_user(login)
