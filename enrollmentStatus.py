#!/home/esmith21/opt/python-3.6.2/bin/python3
from __future__ import absolute_import
from __future__ import print_function
import csv,sys,yaml,duo_client
from six.moves import input
from datetime import datetime

argv_iter = iter(sys.argv[1:])
def get_next_arg(prompt):
    try:
        return next(argv_iter)
    except StopIteration:
        return input(prompt)

##--------------- Vars ---------------
with open("/home/esmith21/.credentials.yaml", 'r') as config_in:
     config = yaml.safe_load(config_in)

admin_api = duo_client.Admin(
    ikey=config['duo']['admin']['ikey'],
    skey=config['duo']['admin']['skey'],
    host=config['duo']['host'],
)
directory_key = config['duo']['directory_key']

# Retrieve user info from API:
users = admin_api.get_users()
users = sorted(users, key = lambda i: i["username"])

# Print CSV of username, phone number, phone type, and phone platform:
#
# (If a user has multiple phones, there will be one line printed per
# associated phone.)
with open(sys.path[0] + '/enrollmentStatus.txt', 'w') as myfile:
  reporter = csv.writer(myfile)
  #print("[+] Report of all users and associated phones:")

  reporter.writerow(('Username', 'Is Enrolled', 'Last Login', 'Phone Number', 'Type', 'Platform'))
  for user in users:
    if user["last_login"] is not None:
      user["last_login"] = datetime.utcfromtimestamp(int(user["last_login"])).strftime('%Y-%m-%d %H:%M:%S')
    phoneNumbers = ''
    phoneTypes = ''
    phonePlatforms = ''
    phoneCount = 0
    for phone in user["phones"]:
      if phoneCount > 0:
        phoneNumbers += "\n"
        phoneTypes += "\n"
        phonePlatforms += "\n"
      phoneNumbers += phone["number"] if (phone["number"] is not '') else "N/A"
      phoneTypes += phone["type"]
      phonePlatforms += phone["platform"]
      phoneCount += 1

    reporter.writerow([
      user["username"], user["is_enrolled"], user["last_login"],
      phoneNumbers, phoneTypes, phonePlatforms,
    ])
