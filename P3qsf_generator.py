import pandas as pd
import matplotlib.pyplot as plt
import re

# Read the out file in the form of
# ResponseID, Last, First, email, External, Q2_1, ..., Q2_37
df=pd.read_csv('AcaP2-Ranking_24samples.csv',keep_default_na=False)
#df.head()
#int(df.at[1,'Q2_1'])
dfT=df.transpose()
[rows,cols] = dfT.shape  # Cols are now series with one respondents info.

question=["Q2_12","Q2_2","Q2_4","Q2_1","Q2_24","Q2_19","Q2_30","Q2_8","Q2_22","Q2_10","Q2_11","Q2_3","Q2_6","Q2_15","Q2_13","Q2_17","Q2_21","Q2_34","Q2_35","Q2_28","Q2_16","Q2_20","Q2_29","Q2_26","Q2_18","Q2_5","Q2_23","Q2_31","Q2_9","Q2_7","Q2_14","Q2_27","Q2_25","Q2_33","Q2_32"]
qsfNumber=[41,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124]

with open('AcaP3-Starter.qsf') as myfile:
    qfile = myfile.read()

# Loop and output a new file which each row  (Should probably do this as a function)
for response in dfT:
    #  dfT[response][3] # email
    #  dfT[response]["Q2_1"]
    responseFile = qfile  # reset response to starting file.
    for j in range(len(qsfNumber)):
        # DBG: print(f"qsfNum {qsfNumber[j]} - response {dfT[response][question[j]]}\n")
        # Note:  regexp are almost always ugly!
        # This is trying to
        # a) find the starting section with default choices
        # b) find the correct number from the shorted array above taken from the order
        #    in the default qsf file
        # c) remove the one character answer
        # d) find the rest of the section
        #   - .*? is a non-greed search (required in my testing)
        #   - fr is "format" and "raw" to allow the variable expansion
        #   - this requires real "{" to be escaped with another "{".  Totally not-expected.
        #   - in the sub, if I did "\1\2{fstring}\3" it always failed, but adding one char
        #     before fstring seems to work.  :-(
        #   - In the match, the last entry will have three "}" instead of two.  Wierd with the "}} stuff to escape."
        if (dfT[response][question[j]] == ""):
            # If the response is blank, remove the "default" for this question.
            # One entry example:  "91":{"5":{"Selected":true}},
            # TBD figure out how to deal with last element (comma problem...) or first (no comman problem).  Final cleanup?
            responseFile = re.sub( \
                fr'("DefaultChoices":{{.*?)"{qsfNumber[j]}":{{"\d{{1}}":{{"Selected":true}}}},?(.*?}}{{1,3}},)', \
                fr'\1\2', \
                responseFile)
        else:
            # With a real response, change the default to the actual number from the Phase 2 data
            responseFile = re.sub( \
                fr'("DefaultChoices":{{)(.*?"{qsfNumber[j]}":{{)"\d{{1}}(":.*?}}}})', \
                fr'\1\2"{dfT[response][question[j]]}\3', \
                responseFile)

    # Cleanup to deal with extra comma if last element is removed.
    responseFile = re.sub( \
                r'("DefaultChoices":{.*?}}),(},"DataExportTag":"Q2",)', \
                fr'\1\2', \
                responseFile)
    # Output this as a new qsf file
    surveyName = "AcaP3-Starter" + str(dfT[response]["RecipientEmail"])
    fileName = f"{surveyName}.qsf"
    responseFile = re.sub( \
        fr'(,"SurveyName":)".*?(","SurveyDescription":null,)', \
        fr'\1"{surveyName}\2', \
        responseFile)
        
    with open(fileName,'w') as outFile:
        outFile.write(responseFile)




