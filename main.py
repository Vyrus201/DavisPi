import time

#import datetime

import pandas as pd

import os

i = 1
while i == 1:
    df1 = pd.read_csv('C:/Users/adpgm/AppData/Local/Programs/Python/Python310/Test for Class HTML.csv')
    print("The dataframe is:")
    print(df1)
    html_string = df1.to_html()

    #Get the Value of Current Weather
    cwlocation = df1.loc[:, "Current Weather"]
    cwlocation_new = str(cwlocation)
    indexcw = cwlocation_new.find("\n")
    act_locationcw = (cwlocation_new[4:indexcw])
    print(act_locationcw)
    intact_locationcw = int(act_locationcw)


    #Get the Value of High Temp
    htlocation = df1.loc[:, "High Temp"]
    htlocation_new = str(htlocation)
    indexht = htlocation_new.find("\n")
    act_locationht = (htlocation_new[4:indexht])
    print(act_locationht)


    # Get the Value of High Temp
    ltlocation = df1.loc[:, "Low Temp"]
    ltlocation_new = str(ltlocation)
    indexlt = ltlocation_new.find("\n")
    act_locationlt = (ltlocation_new[4:indexlt])
    print(act_locationlt)


    # Get the Value of Wind Direction
    wdlocation = df1.loc[:, "Wind Direction"]
    wdlocation_new = str(wdlocation)
    indexwd = wdlocation_new.find("\n")
    act_locationwd = (wdlocation_new[4:indexwd])
    print(act_locationwd)


    # Get the Value of Wind Speed
    wslocation = df1.loc[:, "Wind Speed"]
    wslocation_new = str(wslocation)
    indexws = wslocation_new.find("\n")
    act_locationws = (wslocation_new[4:indexws])
    print(act_locationws)


    # Get the Value of Current Humidity
    chlocation = df1.loc[:, "Current Humidity"]
    chlocation_new = str(chlocation)
    indexch = chlocation_new.find("\n")
    act_locationch = (chlocation_new[4:indexch])
    print(act_locationch)


    # Get the Value of Current Rainfall
    crlocation = df1.loc[:, "Current Rainfall"]
    crlocation_new = str(crlocation)
    indexcr = crlocation_new.find("\n")
    act_locationcr = (crlocation_new[4:indexcr])
    print(act_locationcr)
    intact_locationcr = int(act_locationcr)




    f = open("html_output.html", 'w')



    if intact_locationcr > 0:
        print("Working")
        div0 = """<div style = "position:absolute; left:555px;">"""
        words0 = """<html><head></head><style> body{ background-image: url('Rainfall.jpg'); } </style><body><p><font size = "+2"><b> WXtreme: Weather Station Information</b></font></p>"""
        enddiv0 = """</div>"""
    elif intact_locationcw >= 60:
        print("Working")
        div0 = """<div style = "position:absolute; left:555px;">"""
        words0 = """<html><head></head><style> body{ background-image: url('Sunny.jpg'); } </style><body><p><font size = "+2"><b> WXtreme: Weather Station Information</b></font></p>"""
        enddiv0 = """</div>"""
    elif intact_locationcw <= 32:
        print("Working")
        div0 = """<div style = "position:absolute; left:555px;">"""
        words0 = """<html><head></head><style> body{ background-image: url('Snowy.jpg'); } </style><body><p><font size = "+2"><b> WXtreme: Weather Station Information</b></font></p>"""
        enddiv0 = """</div>"""
    elif intact_locationcw >= 80:
        print("Working")
        div0 = """<div style = "position:absolute; left:555px;">"""
        words0 = """<html><head></head><style> body{ background-image: url('Beach.jpg'); } </style><body><p><font size = "+2"><b> WXtreme: Weather Station Information</b></font></p>"""
        enddiv0 = """</div>"""



    messagesdiv0 = div0
    message0 = words0
    enddivmessage0 = enddiv0




    #THIS IS THE CURRENT WEATHER INFORMATION -- SEPARATED OUT
    divcw = """<div style = "position:absolute;">"""
    wordscw = """<p><font size = "+1"><b>The Current Weather is:</p></b></font>"""
    wordscw1 = act_locationcw
    enddivcw = """</div>"""


    #THIS IS THE HIGH TEMP INFORMATION -- SEPARATED OUT
    divht = """<div style = "position:absolute; top:80px;">"""
    wordsht = """<p><font size = "+1"><b>The High for today is:</p></b></font>"""
    wordsht1 = act_locationht
    enddivht = """</div>"""


    #THIS IS THE HIGH TEMP INFORMATION -- SEPARATED OUT
    divlt = """<div style = "position:absolute; top:160px;">"""
    wordslt = """<font size = "+1"><b><p>The Low for today is:</p></b></font>"""
    wordslt1 = act_locationlt
    enddivlt = """</div>"""


    # THIS IS THE WIND DIRECTION INFORMATION -- SEPARATED OUT
    divwd = """<div style = "position:absolute; top:240px;">"""
    wordswd = """<font size = "+1"><b><p>The current wind direction is:</p></b></font>"""
    wordswd1 = act_locationwd
    enddivwd = """</div>"""


    # THIS IS THE WIND SPEED INFORMATION -- SEPARATED OUT
    divws = """<div style = "position:absolute; top:320px;">"""
    wordsws = """<font size = "+1"><b><p>The current wind speed in mph is:</p></b></font>"""
    wordsws1 = act_locationws
    enddivws = """</div>"""


    # THIS IS THE CURRENT HUMIDITY INFORMATION -- SEPARATED OUT
    divch = """<div style = "position:absolute; top:400px;">"""
    wordsch = """<font size = "+1"><b><p>The current humidity percentage is:</p></b></font>"""
    wordsch1 = act_locationch
    enddivch = """</div>"""


    # THIS IS THE CURRENT RAINFALL INFORMATION -- SEPARATED OUT
    divcr = """<div style = "position:absolute; top:480px;">"""
    wordscr = """<font size = "+1"><b><p>The current rainfall in inches is:</p></b></font>"""
    wordscr1 = act_locationcr
    enddivcr = """</div>"""




    #colordiv = """<div style = "position:absolute; background-color:white;">"""

    #Adds graph/chart to html document

    #div = """<div style = "position:absolute; left:417.8px; top:202.8px;">"""
    #words = html_string
    #enddiv = """</div>"""




    #messagesdiv = div
    #message = words
    #enddivmessage = enddiv





    div2 = """<div style = "position:absolute; left:10px; top:675.8;">"""
    words2 = """<p>Made by the DINO team.</p>"""
    enddiv2 = """</div>"""



    messagesdiv2 = div2
    message2 = words2
    enddivmessage2 = enddiv2


    #div3 = """<div style = "position:absolute; left:417.8; top:280.8;">"""
    #words3 = """<p>This weather station takes real time data and displays it on the chart above.</p>
    #<p>The chart is updated every thirty seconds.</p>"""
    #enddiv3 = """</div>"""



    #messagesdiv3 = div3
    #message3 = words3
    #enddivmessage3 = enddiv3

    endbodyhtml = """</body></html>"""

    #######################THIS SECTION IS WRITE FOR ALL DIV AND MESSAGE VALUES#############################

    #F.WRITE FOR MESSAGE DIV 0
    f.write(messagesdiv0)
    f.write(message0)
    f.write(enddivmessage0)

    #F.WRITE FOR CURRENT WEATHER
    f.write(divcw)
    f.write(wordscw)
    f.write(wordscw1)
    f.write(enddivcw)

    #F.WRITE FOR HIGH TEMP
    f.write(divht)
    f.write(wordsht)
    f.write(wordsht1)
    f.write(enddivht)

    #F.WRITE FOR LOW TEMP
    f.write(divlt)
    f.write(wordslt)
    f.write(wordslt1)
    f.write(enddivlt)

    #F.WRITE FOR WIND DIRECTION
    f.write(divwd)
    f.write(wordswd)
    f.write(wordswd1)
    f.write(enddivwd)

    #F.WRITE FOR WIND SPEED
    f.write(divws)
    f.write(wordsws)
    f.write(wordsws1)
    f.write(enddivws)

    #F.WRITE FOR CURRENT HUMIDITY
    f.write(divch)
    f.write(wordsch)
    f.write(wordsch1)
    f.write(enddivch)

    #F.WRITE FOR CURRENT RAINFALL
    f.write(divcr)
    f.write(wordscr)
    f.write(wordscr1)
    f.write(enddivcr)

    #F.WRITE FOR EVENTUAL COLOR DIV
    #f.write(colordiv)

    #F.WRITE FOR MESSAGE DIV FOR CHART
    #f.write(messagesdiv)
    #f.write(message)
    #f.write(enddivmessage)

    #F.WRITE FOR MESSAGE DIV 2
    f.write(messagesdiv2)
    f.write(message2)
    f.write(enddivmessage2)

    #F.WRITE FOR MESSAGE DIV 3
    #f.write(messagesdiv3)
    #f.write(message3)
    #f.write(enddivmessage3)
    #f.write(endbodyhtml)

    #CLOSE THE FILE AND LOOP AFTER 30 SEC
    f.close()
    print("Time to sleep")
    time.sleep(30)
    print("DONE!!")


