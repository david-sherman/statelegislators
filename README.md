# statelegislators

Assign social media accounts to state legislators from the Open States database using the Google Civic API.

This program assigns social media accounts to the state legislators provided by Open States. For each district in each chamber in
each state provided by Open States,  the legislators in the the district are retrieved from Google, names are matched and 
the accounts are assigned to the Open States legislator.  A json file is produced for each state which lists each legislator,
their Open States id and any associated social media acounts that have been found.

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
 
 
 ### Notes

__Rate Limits__

The Google Civic Information API is rate limited.  A delay, set at one second, is built into each call to
 the API.  Change the delay if Google rate limits are encountered.  
 
 __Name Matching__
 
 Name matching, as implemented, can fail for a variety of reasons.  
 
 1. Civic API names do not include accents.  'Debra Marie Sarinana'  - 'Debra M. Sariñana'
 
 2. The Open States API includes hyphenated names while the Civic api sometimes has only part of the name : 'Katie A. Edwards' -  'Katie Edwards-Walpole'
 
 3.  Suffixes, like jr, sr, III, etc, are stripped out.  Unusual suffixes may appear and prevent a match.

A message is printed when no name match is found.

__Non Numeric District Names__

A few chambers are not directly mappable from OpenStates to Google Civic.  These chambers have
non numeric district names and more research is required to map these to the Google Civic chamber numbering system.   Here are those chambers with a sample value shown for each.
 
    ak upper P 
    dc upper Ward 3    
    md lower 42B     
    ma upper Second Suffolk   
    ma lower Tenth Hampden    
    mn lower 22B       
    nh lower Rockingham 6   
    sd lower 26A      
    vt upper Franklin      
    vt lower Windham-2-2   
    
    
Learn more about the Open States API here: http://docs.openstates.org/en/latest/api/

Learn more about the Google Civic Information API here: https://developers.google.com/civic-information/
 
 The program requires an OpenStates API key and a Google Civic Information API key. StateLegislators
 was built using Python 3.6. 
 
 
 ### Usage 
 __Usage:__   statelegislators.py  openstates_api_key   goggle_civic_api_key
 
 Sample Output :
 
 ```----------------------------------------
fl :  154 open state legislators found
fl :  154 google civic API legislators found
fl :  153 matched legislators
fl :  130 matched legislators with social media accounts
fl :  fl.json
Processing ga
Processing ga upper 56
Pr...
```

 
 
