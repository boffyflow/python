# Import the os module, for the os.walk function
import os
from xml.dom import minidom
 
# Set the directory you want to start from
rootDir = 'Y:/Gocator/3xx0_Calibration'

g3210_ballarray = open('G3210_ballarray.csv','w')
g3506_ballarray = open('G3506_ballarray.csv','w')
g3504_singlesphere = open('G3504_singlesphere.csv','w')
g3210_manualVDE = open('G3210_manualVDE.csv','w')
g3506_manualVDE = open('G3506_manualVDE.csv','w')

for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:

        # find part number & serial reliably

        # pn = '0'
        # serial = '0'
        # if "Id.xml" == fname:
        #     mydoc = minidom.parse( dirName + '/' + fname)
        #     pnelem = mydoc.getElementsByTagName('PartNumber')
        #     if pnelem and pnelem[0].childNodes.length > 0:
        #         pn = pnelem[0].firstChild.data
        #         serial = mydoc.getElementsByTagName('SerialNumber')[0].firstChild.data

        # Ball Array results for 3210 and 3506
        # if "SphereVerReport-Final.xml" == fname:
        #     mydoc = minidom.parse( dirName + '/' + fname)
        #     pn = mydoc.getElementsByTagName('PartNumber')[0].firstChild.data
        #     serial = mydoc.getElementsByTagName('Id')[0].firstChild.data
        #     vde = mydoc.getElementsByTagName('VdeEnv')[0].firstChild.data
        #     if "3210" in pn:
        #         str = pn + ',' + serial + ',' + vde
        #         g3210_ballarray.write( str + '\n')
        #         print( 'G3210 ,',str)
        #     if "3506" in pn:
        #         str = pn + ',' + serial + ',' + vde
        #         g3506_ballarray.write( str + '\n')
        #         print( 'G3506 ,',str)
        
        # Manual 7 position VDE for 3210 and 3506

        # Single Sphere results for 3504

        if "VdeReport_7-scan.xml" == fname:
            pn = '0'
            serial = '0'
            mydoc = minidom.parse( dirName + '/' + fname)
            
#            partnumber = mydoc.getElementsByTagName('PartNumber')[0]
#            if partnumber:
#                if partnumber.hasChildNodes:
#                    pn = partnumber.firstChild.data
            serialnumber = mydoc.getElementsByTagName('Id')[0]
            if serialnumber:
                serial = serialnumber.firstChild.data

            vde = mydoc.getElementsByTagName('VdeEnv')[1].firstChild.data

            if '3210' in pn:
                str = pn + ',' + serial + ',' + vde
                g3210_manualVDE.write( str + '\n')
                print( 'G3210 ,',str)
            elif '3506' in pn:
                str = pn + ',' + serial + ',' + vde
                g3506_manualVDE.write( str + '\n')
                print( 'G3506 ,',str)
            else:
                str = serial + ',' + vde
                g3504_singlesphere.write( str + '\n')
                print( 'G3504 ,',str)


