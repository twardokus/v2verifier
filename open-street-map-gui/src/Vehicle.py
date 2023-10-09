

class Vehicle:
    """Class to represent a vehicle in the GUI"""

    def __init__(self,
                 id_number: int,
                 longitude: float,
                 latitude: float,
                 heading: float) -> None:
        """
        Create a new Vehicle instance

        :param id_number: vehicle ID
        :param longitude: longitude
        :param latitude: latitude
        :param heading: heading in degrees (offset clockwise from 0 being due North)
        """
        self.id_number = id_number
        self.longitude = longitude
        self.latitude = latitude
        self.heading = heading

    def update_position(self,
                        new_longitude: float,
                        new_latitude: float,
                        new_heading: float) -> None:
        """
        Update the position of the vehicle

        :param new_longitude: new longitude coordinate
        :param new_latitude: new latitude coordinate
        :param new_heading: new heading (degrees)
        """
        self.longitude = new_longitude
        self.latitude = new_latitude
        self.heading = new_heading
