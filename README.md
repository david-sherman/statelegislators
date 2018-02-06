# statelegislators

Assign social media accounts to state legislators from the Open States database using the Google Civic API

This program assigns social media accounts to the state legislators provided by the Open States. For each district in each chamber in
each state provided by Open States,  the legislators in the the district are retrieved from Google, names are matched and 
the accounts are assigned to the Open States legislator.  A json file is produced for each state which lists each legislator,
thier Open States id and any associated social media acounts that have been found.

Sample file content from al.json:
```
{
    "state": "al", 
    "upper": [
        {
            "id": "ALL000001", 
            "name": "Gerald H. Allen", 
            "accounts": [
                {"type": "Twitter", "id": "SenGeraldAllen"}
                ]
        }, 
        ...
        {
            "id": "ALL000010", 
            "name": "Gerald O. Dial", 
            "accounts": [
                {"type": "Facebook", "id": "gerald.dial"}
               ]
        }, ... 

``` 
 
 
 Note that the  Google Civic Information API is rate limited.  A delay, set at one second, is built into each call to
 the API.  Change the delay if Google rate limits are encountered,
 
 Learn more about the Open States API here: http://docs.openstates.org/en/latest/api/
 Learn more about the Google Civic Information API here: https://developers.google.com/civic-information/
 
 The program requires an OpenStates API key and a Google Civic Information API key. StateLegislators
 was built using Python 3.6. 
 
 __Usage:__   statelegislators.py  openstates_api_key   goggle_civic_api_key
 
 Sample Output :
 
 