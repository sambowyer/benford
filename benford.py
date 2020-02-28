# A program to check how close records of sql databases
# match up with the Benford's Law
# Made for the 1PS2 extra task in the spring term of 2020

import sqlite3
import math

debug = False

def firstNonZeroDigit(x):
    for i in x:
        if(i in [str(j) for j in range(1,10)]):
            return i
    return "error"

def lastNonZeroDigit(x):
    for i in x[::-1]:
        if(i in [str(j) for j in range(1,10)]):
            return i
    return "error"

def terminal_width():
    import fcntl, termios, struct
    th, tw, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return tw

def readDB(db, tableName, colNo, mode="first"):
    try:
        connection = sqlite3.connect(db)
        cursor = connection.cursor()

        rowCount = 0

        # query has to select entire records and select the desired figure using colNo
        # for this to work for the spotify dataset table 'album' which is formatted weirdly
        selectQuery = "SELECT * from " + tableName

        cursor.execute(selectQuery)

        leadingDigitCount = {"1" : 0, "2" : 0, "3" : 0,
                             "4" : 0, "5" : 0, "6" : 0,
                             "7" : 0, "8" : 0, "9" : 0,
                             "error" : 0}

        record = cursor.fetchone()
        usable = 0
        while(record != None):
            if (debug):
                if(rowCount == 3): print(record)

            if (type(record) == tuple):
                length = record[colNo]

                if (type(length) == float):
                    #print(str(length)[0])
                    if(mode=="last"):
                        leadingDigitCount[lastNonZeroDigit(str(length))] += 1
                    else:
                        leadingDigitCount[firstNonZeroDigit(str(length))] += 1
                    usable += 1

            rowCount += 1
            record = cursor.fetchone()

        cursor.close()

        percentageUsable = (usable*100.0)/(rowCount)
        if (debug): print("%s records usable out of %s (%s percent)" % (usable, rowCount, percentageUsable))
        if (debug): print(leadingDigitCount)

        return leadingDigitCount

    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if (connection):
            connection.close()

def calculateBenford(n):
    expected = {}
    for i in range(1,10):
        expected[str(i)] = int(math.log10(1+(1.0/i))*n)
    if(debug): print(expected)
    return expected

def compare(actual, expected):
    print("Digit  |   Actual     Expected     Error")
    for i in range(1,10):
        e = expected[str(i)]
        a = actual[str(i)]
        error = 100*((a/float(e)) -1.0)
        print(str(i) + "      |   " + str(a).ljust(11) + str(e).ljust(13) + ("%+f" % (error)).ljust(10) + " %")

# albumLengths, n_albumLengths = readDB("billboard-200.db", "albums", 6)
# albumLengthsBenford = calculateBenford(n_albumLengths)
# compare(albumLengthsBenford, albumLengths)
# for i in range(5,13):
#     readDB("billboard-200.db", "acoustic_features", i)

actual = readDB("billboard-200.db", "acoustic_features", 8, mode="last")
actualSize = 0
for i in range(1,10):
    actualSize += actual[str(i)]

expected = calculateBenford(actualSize)
compare(actual, expected)
