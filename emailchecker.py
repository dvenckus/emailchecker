from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/count', methods = ['POST'])
def email_count():
  '''
  expect json post data
  '{ 
      "emails": [ 
        "test.email@gmail.com", 
        "test.email+spam@gmail.com", 
        "testemail@gmail.com",
        "this.is.a.test+100@gmail.com",
        "my.test@gmail.com",
        ...
      ],
  }'
  process each email address, 
  return a count for the number of unique "normalized" email addresses
  also returns a dictionary of the normalized email and the number of variations detected for that email
  '''
  try:
    postdata = request.get_json(silent=True)
    http_code = 200
    processedEmails = {}

    if postdata and len(postdata['emails']):
      for email in postdata['emails']:
        processedEmails = process_email(processedEmails, email)
        
    return json.dumps({'count': len(processedEmails), 'data': str(processedEmails) }), http_code, {'ContentType':'application/json'}
  
  except Exception as e:
    return json.dumps({'Error': 'Missing POST data'}), http_code, {'ContentType':'application/json'}


def process_email(email_dic = {}, email=''):
  '''
  process the email address,
  if new, add it to the dictionary and initialize the counter
  if already in dictionary, increment counter
  '''
  
  # ignore empty
  email = email.strip()
  if not email:
    return email_dic

  # separate the email name from the domain
  email_arr = email.split("@")

  # ignore anything from '+' and following in name
  # remove '." from name
  name = email_arr[0].split("+")[0].replace(".", "")
  domain = email_arr[1]

  # reassemble parsed email address
  rev_email = f"{name}@{domain}"

  # new email, add it an init the count to 0
  if rev_email not in email_dic: 
    email_dic[rev_email] = 0

  # increment the instance counter
  email_dic[rev_email] += 1

  # return the updated dic
  return email_dic
  


if __name__ == "__main__":
    app.run()