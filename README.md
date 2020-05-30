# emailchecker
A simple python Flask webservice doing a count of email addresses

Accept a list of email addresses and return an integer indicating the number of unique email addresses. Where "unique" email addresses means they will be delivered to the same account using Gmail account matching. 

Specifically: Gmail will ignore the placement of "." in the username. And it will ignore any portion of the username after a "+".
Examples:
test.email@gmail.com, test.email+spam@gmail.com and testemail@gmail.com will all go to the same address, and thus the result should be 1.

## Install and Run

Clone this repository.
```
cd ./emailchecker
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
flask run
```

## Input
Post JSON formatted email addresses to the webservice.
Each address will be parsed to be consistent with gmail matching rules.

Default port is 8082 (may be changed in .flaskenv)
```
curl \
--header "Content-Type: application/json" \
--request POST \
--data '{ 
    "email": [ 
      "test.email@gmail.com", 
      "test.email+spam@gmail.com",
      "testemail@gmail.com",
      "this.is.a.test+100@gmail.com",
      "test.email+this.is.a.test+100@gmail.com",
      "my.test@gmail.com"
    ] 
}' http://127.0.0.1:8082/count
```

## Output
Results are returned in JSON format.

**count**:     integer.     The number of unique email address matches

**matched**:   dictionary.  The matched email addresses and the number of occurences of each match.
```
{ 
  "count": 3, 
  "matched": "{
    'testemail@gmail.com': 4, 
    'thisisatest@gmail.com': 1, 
    'mytest@gmail.com': 1
  }
}
```

