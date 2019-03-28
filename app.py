from __future__ import print_function

import flask

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import quandl
quandl.ApiConfig.api_key = "u1z3S_H23FTDr32ryHpR"


app = flask.Flask(__name__)

def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

@app.route("/")
def get_plot_stock_data():
    """ Very simple embedding of closing price data from Quandl
    """
    # Grab the inputs arguments from the URL
    args = flask.request.args

    # Get all the form arguments in the url with defaults
    Tick = getitem(args, 'Tick', 'GOOG')
    _from = getitem(args, '_from', '2016-01-01')
    to = getitem(args, 'to', '2016-01-31')
    
    # Create line graph with those arguments
    data = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['ticker', 'date', 'close'] }, 
                                                    ticker = [Tick], date = { 'gte': _from, 'lte': to })
  
    x = data['date']
    Y = data['close']
    
    TOOLTIPS=[("Date","$X"),("Closing Price","$Y"),]
    
    fig = figure(title="Closing Price of "+Tick+" from "+_from+" to "+to,x_axis_type='datetime',
                 x_axis_label='Date',y_axis_label='Closing Price')
    fig.line(x, Y, color='#000000', line_width=2)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)
    html = flask.render_template(
        'home.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        #Ticker=T,
        _from=_from,
        Tick=Tick,
        to=to
    )
    return encode_utf8(html)

if __name__ == "__main__":
    print(__doc__)
    app.run()