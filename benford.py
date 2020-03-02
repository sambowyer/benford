# A collection of functions designed to make it easy to
# check large datasets for occurences of Benford's Law
# Made for the 1PS2 extra task in the spring term of 2020

import sqlite3
import math

def firstNonZeroDigit(x):
    for i in x:
        if(i in [str(j) for j in range(1,10)]):
            return i
    return "error"

def readDB(db, tableName, colNo, mode="first"):
    leadingDigitCount = {"1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0,
                         "6" : 0, "7" : 0, "8" : 0, "9" : 0, "error" : 0}
    try:
        connection = sqlite3.connect(db)
        cursor = connection.cursor()

        selectQuery = "SELECT * from " + tableName

        cursor.execute(selectQuery)

        record = cursor.fetchone()
        while(record != None):

            if (type(record) == tuple):
                length = record[colNo]

                if (type(length) == float):
                    leadingDigitCount[firstNonZeroDigit(str(length))] += 1
            record = cursor.fetchone()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if (connection):
            connection.close()
    return leadingDigitCount

def mergeDictionaries(a, b):
    for i in b:
        a[i] += b[i]
    return a

def observationsUsed(l):
    total = 0
    for i in l:
        if i != "error":
            total += l[i]
    return total

def calculateBenford(n, base=10):
    expected = {}
    for i in range(1,base):
        expected[str(i)] = int(math.log(1+(1.0/i), base)*n)
    return expected

def compare(actual, expected):
    print("Digit  |   Actual     Expected     Error")
    for i in range(1,10):
        e = expected[str(i)]
        a = actual[str(i)]
        error = 100*((a/float(e)) -1.0)
        print(str(i) + "      |   " + str(a).ljust(11) + str(e).ljust(13)
                     + ("%+f" % (error)).ljust(10) + " %")
