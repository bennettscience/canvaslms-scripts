from config import PROD_URL, PROD_KEY
from canvasapi import Canvas

canvas = Canvas(EACC_URL, EACC_KEY)

# Run a quick loop and make some dummy students
account = canvas.get_account(1)

for i in range(1, 5):
    # Create a user object
    user = {
        'name': 'Test Student ' + str(i),
        'terms_of_use': True,
        'skip_registration': True,
    }

    # Update the user login info
    pseudonym = {
        'unique_id': 'tstudent' + str(i),
        'password': 'tstudent' + str(i),
        'send_confirmation': False,
    }

    try:
        account.create_user(pseudonym, user=user)
        print(f'Successfully created {user['name']}')
    except Exception as e:
        print(e)


