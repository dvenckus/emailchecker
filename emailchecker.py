from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/count', methods = ['POST'])
def email_count():
  '''
  INPUT json post data
    '{ 
        "email": [ 
          "test.email@gmail.com", 
          "test.email+spam@gmail.com", 
          "testemail@gmail.com",
          "this.is.a.test+100@gmail.com",
          "my.test@gmail.com",
          ...
        ],
    }'
  
  OUTPUT 
  count:    (integer) number of matched email addresses
  matched:  (dictionary) the matched emails and the number of occurences of each email
  '''
  try:
    postdata = request.get_json(silent=True)
    http_code = 200
    matched_emails = {}

    if postdata and len(postdata['email']):
      for email in postdata['email']:
        matched_emails = do_email_matching(matched_emails, email)
        
    return json.dumps({'count': len(matched_emails), 'matched': str(matched_emails) }), http_code, {'ContentType':'application/json'}
  
  except Exception as e:
    http_code = 400
    return json.dumps({'Error': str(e)}), http_code, {'ContentType':'application/json'}


def do_email_matching(matched_emails = {}, email=''):
  '''
  process the email address,
  if new, add it to the dictionary and initialize the counter
  if already in dictionary, increment counter
  '''
  
  # ignore empty
  email = email.strip()
  if not email:
    return matched_emails

  # separate the email name from the domain
  email_arr = email.split("@")

  # ignore anything from '+' and following in name
  # remove '." from name
  name = email_arr[0].split("+")[0].replace(".", "")
  domain = email_arr[1]

  # reassemble parsed email address
  rev_email = f"{name}@{domain}"

  if rev_email in matched_emails: 
    # increment existing email
    matched_emails[rev_email] += 1 
  else:
    # initialize new email
    matched_emails[rev_email] = 1

  # return the updated dic
  return matched_emails
  


if __name__ == "__main__":
    app.run()