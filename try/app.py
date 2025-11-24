from bokeh.plotting import curdoc
from bokeh.layouts import column
from bokeh.models import Button
import bokeh.palettes as pals

from threading import Thread
import random
import time

import topo_fig

plots = topo_fig.plot_dags()
pal = pals.Category20c[20]

doc = curdoc()

def on_button():
    ds = doc.get_model_by_name('circles_1').data_source
    data = dict(ds.data)
    # print(ds)
    # print(data)
    n = len(ds.data['state'])
    newpal = random.choices(pal, k=n)

    patch = {'state': [(slice(n), newpal)]}
    ds.patch(patch)

    # data['state'] = newpal
    # ds.data = data

    # time.sleep(1)
    print('button')

button = Button(label='Palette')
button.on_event('button_click', on_button)

curdoc().add_root(column(button, *[plot for plot in plots]))

def update():
    print('update')
    ds = doc.get_model_by_name('circles_1').data_source
    data = dict(ds.data)
    # print(ds)
    # print(data)
    n = len(ds.data['state'])
    newpal = random.choices(pal, k=n)
    patch = {'state': [(slice(n), newpal)]}
    ds.patch(patch)

def spin():
    while True:
        time.sleep(1)
        print('spin')
        doc.add_next_tick_callback(update)

thread = Thread(target=spin)
thread.start()
