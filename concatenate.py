import sys
import argparse
import os
import time

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('f1', help='file 1')
    parser.add_argument('f2', help='file 2')
    parser.add_argument('f3', help='file 3')
    parser.add_argument('of', help='output file')
   
    args = parser.parse_args()
    
    file1 = 'rs0000' + args.f1 + '.csv'
    file2 = 'rs0000' + args.f2 + '.csv'
    file3 = 'rs0000' + args.f3 + '.csv'

    print( file1)
    print( file2)
    print( file3)

    filenames = [file1, file2, file3]
    with open( args.of + '.csv', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

if __name__ == "__main__":

    main()
