# -*- coding: utf-8 -*-
def classFactory(iface):
    from .round_coordinates import RoundCoordinates
    return RoundCoordinates(iface)