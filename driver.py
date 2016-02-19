from location import Location, manhattan_distance
from rider import Rider


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    @type id: str
        A unique identifier for the driver.
    @type location: Location
        The current location of the driver.
    @type is_idle: bool
        A property that is True if the driver is idle and False otherwise.
    """

    def __init__(self, identifier, location, speed):
        """Initialize a Driver.

        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None
        """
        # TODO
        self.id  = identifier
        self.location = location
        self.speed = speed
        self.destination = None

    def __str__(self):
        """Return a string representation.

        @type self: Driver
        @rtype: str
        >>> driver = Driver("Bob",Location(5,10), 10)
        >>> print(driver)
        Driver: Bob, located at 5,10
        """
        # TODO
        return "Driver: {0}, located at {1}".format(self.id,self.location)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Driver
        @rtype: bool
        """
        # TODO
        pass

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int
        >>> driver1 = Driver("driver1",Location(5,10), 10)
        >>> driver1.location = Location(5,6)
        >>> destination = Location(8,3)
        >>> driver1.speed = 3
        >>> driver1.get_travel_time(destination)
        2
        """
        # TODO
        return manhattan_distance(self.location,destination) // self.speed

    def start_drive(self, location):
        """Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int
        >>> driver1 = Driver("driver1",Location(5,10), 10)
        >>> location = Location(4,8)
        >>> driver1.destination = Location(2,6)
        >>> driver1.speed = 2
        >>> print(driver1.start_drive(location))
        1
        """
        # TODO
        self.destination = location
        return manhattan_distance(self.location,self.destination) // self.speed

    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        # TODO
        #not sure if complete
        self.location = self.destination

    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int

        >>> driver = Driver("driver",Location(5,10), 10)
        >>> driver.location = Location(20,5)
        >>> driver.speed = 5
        >>> rider = Rider("rider","waiting",Location(5,15),Location(20,5),100)
        >>> driver.start_ride(rider)
        5
        """
        # TODO
        self.destination = rider.destination
        return manhattan_distance(self.location,rider.destination) // self.speed


    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        # TODO
        self.location = self.destination
        self.destination = None
