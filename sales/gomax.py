import pandas as pd
import numpy as np
import locale

############# Settings ########################################

# input file names (required)
datadir = 'data/'
customerdb = datadir + 'customer_list.csv'

# time window
startdate = '2015-01-01'
enddate = '2030-12-31'

###############################################################

def vcount( df, column):

    arr = {}

    for index, row in df.iterrows():
        key = row[column]
        if key in arr:
            arr[ key] += row['Quantity']
        else:
            arr[ key] = row['Quantity']

    return arr


def quarterly( df):

    dfq = df.drop( columns=['Date', 'Brand', 'Subsidiary', 'Partnumber', 'Customer', 'ASP'])
    dfq = dfq.groupby( 'Quarter').agg({'Quantity': 'sum', 'Amount': 'sum', 'AMERICAS': 'sum', 'EMEAR': 'sum', 'APAC': 'sum'})
    dfq['ASP'] = dfq.Amount / dfq.Quantity

    return dfq


def build_df( data, regions):

    clist = pd.read_csv( regions)
    df = pd.read_csv( data)

    # convert strings into datetime objects
    df['Date'] = pd.to_datetime( df['Date'])

    # filter out the entries based on start and end date
    df = df.loc[( df['Date'] >= startdate) & ( df['Date'] <= enddate)]

    df = df.drop( columns=['Document Number', 'Product Series', 'SO Type'])
    df = df.rename( columns={'Company Name': 'Customer', 'Item': 'Partnumber', 'Amount (Net)': 'Amount', 'Subsidiary (no hierarchy)': 'Subsidiary'})
    df = df.drop( df[df.Amount <= 0.0].index)
    df = df.drop( df[df.Customer == 'Total'].index)

    # check if all the customers are the customerdb
    err = False
    for row in df.itertuples():
        if( row.Customer not in clist['Customer'].to_numpy()):
            print( row.Customer, 'not found in the customer db. Please update customer_list.csv')
            err = True
    if err:
        print( 'Exiting application due to missing customer(s)!')
        raise SystemExit

    df.Date = pd.to_datetime( df.Date)
    df['Quarter'] = pd.PeriodIndex( df.Date, freq='Q')
    df['ASP'] = df.Amount / df.Quantity
    df = df.merge( clist)
    df['AMERICAS'] = 0
    df['EMEAR'] = 0
    df['APAC'] = 0

    for index in df.index:
        df.at[ index, 'AMERICAS'] = df.at[ index, 'Quantity'] if df.at[ index, 'Region'] == 'AMERICAS' else 0
        df.at[ index, 'EMEAR'] = df.at[ index, 'Quantity'] if df.at[ index, 'Region'] == 'EMEAR' else 0
        df.at[ index, 'APAC'] = df.at[ index, 'Quantity'] if df.at[ index, 'Region'] == 'APAC' else 0

    df = df.sort_values( 'Quarter', ascending=True)

    return df


def df_stats( df, fname = 'tmp.csv'):

    fp = open( fname, 'w')

    fp.write( 'total sales,' + str( round( df['Amount'].sum(), 2)) + '\n')
    fp.write( 'total sensors,' + str( df['Quantity'].sum()) + '\n')
    fp.write( 'average sensor price,' + str( round( df['Amount'].sum() / df['Quantity'].sum(), 2)) + '\n')

    print( '\nCustomer,Number', file=fp)
    n = 10
    arr = vcount( df, 'Customer')
    for key, value in sorted( arr.items(), key=lambda item: item[1], reverse=True)[:n]:
        print( '\"%s\", %s' % (key, value), file=fp)

    print( '\nRegion,Number', file = fp)
    n = 3
    arr = vcount( df, 'Region')
    for key, value in sorted( arr.items(), key=lambda item: item[1], reverse=True)[:n]:
        print( '\"%s\", %s' % (key, value), file=fp)
    
    print( '\nBrand,Number', file = fp)
    n = 10
    arr = vcount( df, 'Brand')
    for key, value in sorted( arr.items(), key=lambda item: item[1], reverse=True)[:n]:
        print( '\"%s\", %s' % (key, value), file=fp)

    print( '\nPartnumber,Number', file = fp)
    n = 10
    arr = vcount( df, 'Partnumber')
    for key, value in sorted( arr.items(), key=lambda item: item[1], reverse=True)[:n]:
        print( '\"%s\", %s' % (key, value), file=fp)


def main():

    locale.setlocale( locale.LC_ALL, '')
    print( '\nOutput from', startdate, 'to', enddate, ':\n')

    fname = datadir + 'GoMax.csv'
    df = build_df( fname, customerdb)
    df.to_csv( datadir + 'GoMax_all.csv')
    quarterly( df).to_csv( datadir + 'GoMax_quarterly.csv')
    df_stats( df, datadir + 'GoMax_stats.csv')
    print( '****** GoMax ******')
    print( 'total sales:', locale.currency( df['Amount'].sum(), grouping=True))
    print( 'total sensors: %d' % df['Quantity'].sum())
    print( 'average sensor price:', locale.currency( df['Amount'].sum() / df['Quantity'].sum(), grouping=True), '\n')


if __name__ == "__main__":
    main()


