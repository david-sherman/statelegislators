import requests
from urllib.parse import quote
from time import sleep
import json
import sys


class openstates():
    headers = None
    base_url = "https://openstates.org/api/v1/"

    def __init__(self, api_key):
        self.headers =  {'X-API-KEY': api_key}

    def fetch(self, url):
        result = requests.get(url,headers=self.headers)
        return json.loads(result.text)

    def stateLegislators(self, state, chamber ):
        url = "%s%s?state=%s&chamber=%s" % (self.base_url, "legislators", state, chamber)
        return self.fetch(url)

    def metatdata(self):
        url = "%s/metadata" % (self.base_url)
        return self.fetch(url)

class google():

    api_key = ""
    civic_template = "https://www.googleapis.com/civicinfo/v2/representatives/%s?key=%s&recursive=true"
    sleep = 1   # seconds to sleep between calls to the google civi api. The api is definitely rate limited

    def __init__(self,api_key):
        self.api_key = api_key

    def stateLegislators(self, state,chamber,district):
        sleep( self.sleep)
        oc_id = "ocd-division/country:us/state:%s/sld%s:%s" % (state, chamber[0:1], district)
        url = self.civic_template % (quote(oc_id, safe=""), self.api_key)
        result = requests.get(url)
        payload =  json.loads(result.text)
        if 'error' in payload:
            print( "ERROR")
            print ( payload["error"]["errors"][0])
            print( "Adjust global sleep parameter ")
            sys.exit(1)
        return payload


class stateClass():

    openstates = None
    abbreviation = None
    chambers = [ 'upper','lower']
    resultset = {}
    openstateLegislatorCount = 0
    civicLegislatorCount = 0
    matched = 0
    matched_with_accounts = 0


    def __init__(self,oso,civic,abbreviation):
        self.openstates = oso
        self.civic = civic
        self.abbreviation = abbreviation
        self.resultset = { 'state': self.abbreviation , "upper" : [], "lower" : []}
        print("Processing %s" % self.abbreviation)

    def processDistrict(self, chamber, district, openstatesLegislators):
        print( "Processing %s %s %s " % (self.abbreviation, chamber, district))
        districtLegislators =  self.civic.stateLegislators(self.abbreviation,chamber,district)
        if not "officials" in districtLegislators:
            print(
                "CIVIC API returns no officials found for state %s chamber %s district %s" % (self.abbreviation, chamber, district))
            print(districtLegislators)
            return None

        matched = 0
        for official in districtLegislators["officials"]:
            self.civicLegislatorCount = self.civicLegislatorCount + 1

            # There may be no social media accounts associated with this legislator
            # process the person anyway.

            accounts = []
            if "channels" in official: accounts = official["channels"]

            # determine the last name.  Strip out punctuation and extra words

            name = ''.join(ch for ch in official['name'] if ch not in set( '.,'))
            components = name.lower().split(" ")
            components.reverse()
            if components[0] in ['jr', 'sr', 'ii', 'iii', 'iv', 'phd', 'esq', 'md']: components.pop(0)
            last_name = components[0]


            for person in openstatesLegislators:
                openstatesname = person['first_name']  + " " + person['last_name']
                # Two ways names can match.  (1) they simply do as in : "Robert Van Wagner" == "Robert Van Wagner"
                # or  (2) their last names math as in :  "Julio E. Rodriguez Jr.  == "Rodriguez"

                if ( openstatesname == name ) or person['last_name'].lower() == last_name :
                    self.resultset[chamber].append( { "id" : person["id"], "name" : openstatesname, "accounts" : accounts})

                    matched = matched + 1
                    self.matched = self.matched + 1
                    if (len(accounts) > 0 ) :
                        self.matched_with_accounts  = self.matched_with_accounts + 1

        if matched  != len(openstatesLegislators):
            print("%s %s district '%3s' matched %s of %s." % (self.abbreviation, chamber, district, matched, len(openstatesLegislators)))
            for official in  districtLegislators["officials"]:
                print( " --- civic :'%s'"  % official['name'] )
            for person in openstatesLegislators:
                print( " --- openstates : '%s %s'" % (person['first_name'],person['last_name']))

    def processChamber(self, chamber, legislators):
        chambermap = {}

        for person in legislators:
            self.openstateLegislatorCount = self.openstateLegislatorCount + 1
            district =  str(person["district"])
            if not district in chambermap:
                chambermap[district] = []
            bucket = chambermap[district]
            bucket.append(person)
        for district in chambermap:
            if not district.isnumeric():
                print("skipping %s %s district '%s'" % (self.abbreviation, chamber, district))
            else:
                self.processDistrict(chamber,district,chambermap[district])

    def process(self):
        for chamber in self.chambers:
            self.processChamber(chamber, oso.stateLegislators(self.abbreviation,chamber))

        filename = "%s.json" % self.abbreviation
        with open(filename, 'w') as outfile:
            json.dump(self.resultset, outfile)
        print("----------------------------------------")
        print( "%s :  %s open state legislators found" % (self.abbreviation, self.openstateLegislatorCount ))
        print( "%s :  %s google civic API legislators found" % (self.abbreviation, self.civicLegislatorCount ))
        print( "%s :  %s matched legislators" % (self.abbreviation, self.matched ))
        print( "%s :  %s matched legislators with social media accounts" % (self.abbreviation, self.matched_with_accounts ))
        print( "%s :  %s " % ( self.abbreviation, filename ))


###################################
if len(sys.argv) != 3 :
    print( "Usage :  statelegislators.py openstates_api_key google_civic_api_key" )

oso = openstates( sys.argv[1])
civic = google(sys.argv[2])
states = oso.metatdata()

for item in states:
    state = stateClass(oso, civic, item["abbreviation"])
    state.process()

