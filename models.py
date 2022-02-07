class Park(object):
    park_id = 0
    address = ""
    services = []
    position = None

    def __init__(self, park_id, address, services, latitude, longitude):
        self.park_id = park_id
        self.address = address
        self.services = services
        self.position = Point(latitude, longitude)


class Point(object):
    latitude = None
    longitude = None

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


def convert_park_to_dict(park):
    park_dict = {}
    for attr in vars(park):
        attr_value = getattr(park, attr)
        if isinstance(attr_value, Point):
            point_dict = vars(attr_value)
            park_dict[attr] = point_dict
        else:
            park_dict[attr] = attr_value
    return park_dict
