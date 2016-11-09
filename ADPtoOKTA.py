import csv
from okta import UsersClient
from okta.models.user import User

usersClient = UsersClient("https://flagshipcredit.oktapreview.com", "00NWlAD-Ftc1rYsT1-i044JTwa6FFopZkHvCyVrx5s")

#Create the new user
with open('sample.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        first = (row['first'])
        last = (row['last'])
        login = (row['login'])
        email = (row['email'])
        mobileNum = (row['mobile'])

        user = User(login=login,
                email=email,
                firstName=first,
                lastName=last,
                mobilePhone=mobileNum)

        user = usersClient.create_user(user, activate=False)

#Make sure user was created
#with open('sample.csv') as csvfile:
#    reader = csv.DictReader(csvfile)
#    for row in reader:
#        class okta.UsersClient("https://flagshipcredit.oktapreview.com", "00NWlAD-Ftc1rYsT1-i044JTwa6FFopZkHvCyVrx5s")
#            login = (row['login'])
#            get_user(login)
