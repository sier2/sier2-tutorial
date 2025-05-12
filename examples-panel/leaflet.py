# Demonstrate ipyleaflet in a block.
#
# Requires up-to-date ipywidgets 8.1.7, ipyleaflet 0.19.2, ipywidgets_bokeh 1.6.0.
#

from sier2 import Block, Connection
from sier2.panel import PanelDag

import param

from dataclasses import dataclass
from ipywidgets import HTML
import ipyleaflet as leaflet

import panel as pn

@dataclass
class Location:
    name: str
    lon: float
    lat: float

    @property
    def latlon(self):
        return self.lat, self.lon

cbr = Location('Canberra', 149.131393, -35.280781)
hob = Location('Hobart', 147.325, -42.880556)
mel = Location('Melbourne', 144.946457, -37.840935)
syd = Location('Sydney', 151.209290, -33.868820)

class Inputs(Block):
    """User input of location."""

    in_loc = param.Selector(objects=[cbr, hob, mel, syd])

    out_lon = param.Number(doc='Longitude', bounds=(-180, 180))
    out_lat = param.Number(doc='Latitude', bounds=(-90, 90))

    def __init__(self):
        super().__init__(block_pause_execution=True)

    def execute(self):
        loc = self.in_loc
        self.out_lon = loc.lon
        self.out_lat = loc.lat

class MapBlock(Block):
    """Draw a map."""

    in_lon = param.Number(doc='Longitude', bounds=(-180, 180))
    in_lat = param.Number(doc='Latitude', bounds=(-90, 90))

    def __init__(self):
        super().__init__(name='South-east Australia')
        self.map = leaflet.Map(zoom=9, scroll_wheel_zoom=True)
        poly = leaflet.Polygon(
            locations=[mel.latlon, hob.latlon, syd.latlon],
            color='blue', fill_color='#00000000'
        )
        self.map.add(poly)

        marker = leaflet.Marker(location=cbr.latlon, draggable=False)
        msg = HTML()
        msg.value = 'Hello <b><span style="text-decoration: underline red">world</span></b>'
        marker.popup = msg
        self.map.add(marker)

    def execute(self):
        self.map.center = self.in_lat, self.in_lon

    def __panel__(self):
        return pn.pane.IPyLeaflet(self.map)

if __name__=='__main__':
    inp = Inputs()
    mapb = MapBlock()
    dag = PanelDag(title='Leaflet map', doc='Leaflet demo')
    dag.connect(inp, mapb, Connection('out_lon', 'in_lon'), Connection('out_lat', 'in_lat'))

    dag.show()
