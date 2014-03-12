#!/usr/bin/python
"""Script can be used to calculate the Gini Index of a column in a CSV file.
Classes are strings."""

"""Please set the path variable before running the code."""

import fileinput
import csv
from collections import Counter
from collections import defaultdict

(
    CMTE_ID, AMNDT_IND, RPT_TP, TRANSACTION_PGI, IMAGE_NUM, TRANSACTION_TP,#6
    ENTITY_TP, NAME, CITY, STATE, ZIP_CODE, EMPLOYER, OCCUPATION,
    TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID, CAND_ID, TRAN_ID, FILE_NUM,
    MEMO_CD, MEMO_TEXT, SUB_ID
) = range(22)

CANDIDATES = {
    'P80003338': 'Obama',
    'P80003353': 'Romney',
}

############### Set up variables
gini = 0
zipcode = defaultdict(Counter)
groups = Counter()
path = "C:\\Dropbox\\Spring 2014\\290A - MINING\\data\\pas212\\itpas2.txt"
total = 0

############### Read through files
for row in csv.reader(fileinput.input(path), delimiter='|'):
    candidate_id = row[CAND_ID]
    if candidate_id in CANDIDATES and row[ZIP_CODE]!='': # Ignoring null zip code values
        groups[row[CAND_ID]] += 1
        zipcode[row[ZIP_CODE]][row[CAND_ID]] += 1

# print zipcode.values()[:10]
# print type(zipcode)
# print zipcode

# Function to calculate Gini index
def gini_index_calc(groups):
    """Calculates the Gini Index given a dictionary of class names to counts"""
    total = sum(groups.values())
    return 1 - sum( (float(g)/total)**2 for g in groups.values())

gini = gini_index_calc(groups) # Gini index by Candidate name
total = sum(cnt for zp in zipcode.values() for cnt in zp.values()) # Calculating total of rows
# Since the question doesn't mention if we want a multiway split or binary split. I am assuming multiway split. This means, the groups will be same as number of zipcodes for each candidate. For binary, two groups are created. One group contains the zipcode, other group contains all other zip codes. I am assuming multiway and calculating it for all zipcode classes.
split_gini = sum( sum(cl.values()) * gini_index_calc(cl) for cl in zipcode.values()) / total

print "Total number of records for candidates",total
print "Records for",CANDIDATES.values()[0],groups.values()[0]
print "Records for",CANDIDATES.values()[1],groups.values()[1]
print
print "Gini Index: %s" % gini

# print len(zipcode)

print """
Since the question doesn't mention if we want a multiway split or binary split. I am assuming multiway split. This means, the groups will be same as number of zipcodes for each candidate. For binary, two groups are created. One group contains the zipcode, other group contains all other zip codes. I am assuming multiway and calculating it for all zipcode classes.
"""

print "Gini Index after split(multiway split on zipcode): %s" % split_gini


"""OUTPUT
Total number of records for candidates 52451
Records for Romney 22106
Records for Obama 30345

Gini Index: 0.487662946024

Since the question doesn't mention if we want a multiway split or binary split. I am assuming multiway split. This means, the groups will be same as number of zipcodes for each candidate. For binary, two groups are created. One group contains the zipcode, other group contains all other zip codes. I am assuming multiway and calculating it for all zipcode classes.

Gini Index after split(multiway split on zipcode): 0.412986663328

"""
