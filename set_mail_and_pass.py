import os
def set_environment_variables():
    '''
    This function prompts the user to enter their email and password if they are not already stored in the system's environment variables. It then saves these values as environment variables.
    '''
    email = os.environ.get('mymail')
    password = os.environ.get('myapp_pass2')

    if not email:
        email = input("Please enter your email address: ")
        os.environ['mymail'] = email

    if not password:
        password = input("Please enter your email password: ")
        os.environ['myapp_pass2'] = password

set_environment_variables()
