import os,sys,time

if __name__ == '__main__':

    for filename in os.listdir('.'):
        if filename.endswith(".csv"):
            bfn = os.path.splitext(filename)[0]
            print(bfn)
            cmd = 'C:\\Users\\RUebbing\\Documents\\develop\\old\\14405-4.4.4.40_SOFTWARE_GO_Tools\\CsvConverter\\kCsvConverter.exe --csv ' + bfn + '.csv --out ' + bfn + '.obj --format 10'
            print(cmd)
            os.system(cmd)
            time.sleep(900)
            continue
        else:
            continue