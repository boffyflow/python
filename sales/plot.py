import numpy as np
import matplotlib.pyplot as plt

def piePlot( values, labels, fname):

    fig, ax = plt.subplots( figsize=( 6, 3), subplot_kw=dict( aspect="equal"))

    def func( pct, allvals):
    #       absolute = int( pct / 100. * np.sum( allvals))
        return '{:.1f}%'.format( pct)
            
    wedges, texts, autotexts = ax.pie( values, autopct=lambda pct: func(pct, values),
            textprops=dict(color="w"))

    ax.legend( wedges, labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp( autotexts, size=8, weight="bold")
    
    title = fname.split( '/')[1].split( '_')[0] + ' ' + fname.split( '/')[1].split( '_')[1].capitalize()
    
    ax.set_title( title)

    plt.savefig( fname)
