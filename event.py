from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location,Location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp #If the timestamps are equal then the events are equal

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other#If the negation of the object being equal is true then the objects are not equal

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp#Checks if timestamp is smaller than the other one

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp#Checks if timestamps are less than or equal to each other

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other#Checks if timestamp is greater than the other one

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other#Checks if timestamps are greater than or equal to each other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.id, self.rider.location)

        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            dispatcher.deActivateDriver(driver)
            travel_time = driver.start_drive(self.rider.location)
            events.append(Pickup(self.timestamp + travel_time, self.rider, driver))
        events.append(Cancellation(self.timestamp + self.rider.patience, self.rider))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str
        """
        return "{} -- {}: Request a driver".format(self.timestamp, self.rider)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @type self: DriverRequest
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        >>> dispatch = Dispatcher()
        >>> monitor = Monitor()
        >>> rider1 = Rider("rider","waiting",Location(5,15),Location(20,5),10000)
        >>> driver1 = Driver("driver1",Location(5,10), 100)
        >>> driverrequest1 = DriverRequest(15,driver1)
        >>> eventsList = driverrequest1.do(dispatch,monitor)
        >>> driver1.destination = rider1.location
        >>> print(eventsList)
        fdfd
        """
        # Notify the monitor about the request.

        # Request a rider from the dispatcher.
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.
        # TODO

        monitor.notify(self.timestamp, DRIVER, REQUEST,
                       self.driver.id, self.driver.location)
        rider = dispatcher.request_rider(self.driver)
        events = []
        #start drive and create pick up event, the pick up event do() creates the drop off event!!
        if rider is not None:#When a driver is requested the driver that takes the shortest time to get
            dispatcher.deActivateDriver(self.driver)#to the rider will get that assignment
            expectedTravelTime = self.driver.start_drive(rider.location)
            events.append(Pickup(expectedTravelTime + self.timestamp,rider,self.driver))
            #print(expectedTravelTime)
        return events
    def __str__(self):
        """Return a string representation of this event.

        @type s elf: DriverRequest
        @rtype: str
        >>> print(DriverRequest(5,Driver("driver",Location(5,10), 10)))
        5 -- Driver: driver, located at 5,10: Request a rider
        """
        return "{} -- {}: Request a rider".format(self.timestamp, self.driver)


class Cancellation(Event):
    #TODO
    def __init__(self,timestamp,rider):
        """Initialize a Cancellation event.

        @type self: Cancellation
        @type timestamp: integer
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Carries out the cancellation if driver can not make it in time.

        @type self: Cancellation
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        >>> dispatch = Dispatcher()
        >>> monitor = Monitor()
        >>> rider1 = Rider("rider","waiting",Location(5,15),Location(20,5),1)
        >>> driver1 = Driver("driver1",Location(5,10), 10)
        >>> driverrequest1 = DriverRequest(15,driver1)
        >>> eventsList = driverrequest1.do(dispatch,monitor)
        >>> cancellation = Cancellation(16,rider1)
        >>> eventList = cancellation.do(dispatch,monitor)
        >>> print(eventsList)
        []
        """
        events = []
        if self.rider.status != SATISFIED:#Can only be carried out the status of the rider is not SATISFIED
            monitor.notify(self.timestamp, RIDER, CANCEL,self.rider.id,self.rider.location)
            dispatcher.cancel_ride(self.rider)
            self.rider.updateStatus(CANCELLED)

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: Cancellation
        @rtype: str
        >>>
        >>>
        >>> print(Cancellation(dispatch,monitor)
        5 -- Driver: driver, located at 5,10: Request a rider
        """
        return "{} -- {}: Cancellation".format(self.timestamp, self.rider)

class Pickup(Event):
    #TODO
    def __init__(self,timestamp,rider,driver):
        """Initializes a Pickup event.

        @type self: Pickup
        @type rider: Rider
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver
        self.rider = rider

    def do(self,dispatcher,monitor):
        """Carries out the Pickup event when it is called.

        @type self: Pickup
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        >>> dispatch  = Dispatcher()
        >>> monitor = Monitor()
        >>> driver1 = Driver("driver1",Location(5,10), 10)
        >>> rider1 = Rider("rider1","cancelled",Location(5,15),Location(20,5),1)
        >>> pickup = Pickup(15,rider1,driver1)
        >>> eventList = pickup.do(dispatch,monitor)
        >>> driver1.location = rider1.location
        >>> print(eventList[0])
        15 -- Driver: driver1, located at 20,5: Request a rider
        >>> dispatch  = Dispatcher()
        >>> monitor = Monitor()
        >>> driver2 = Driver("driver2",Location(5,10), 10)
        >>> rider2 = Rider("rider2","waiting",Location(5,15),Location(20,5),1)
        >>> pickup = Pickup(15,rider2,driver2)
        >>> eventList = pickup.do(dispatch,monitor)
        >>> driver2.destination = rider2.destination
        >>> print(eventList[0])
        15 -- Driver: driver1, located at 20,5: Request a rider
        """
        self.driver.end_drive()

        events = []
        if self.rider.status == WAITING:
            monitor.notify(self.timestamp,RIDER,PICKUP,self.rider.id,self.rider.location)
            monitor.notify(self.timestamp,DRIVER,PICKUP,self.driver.id,self.driver.location)#ASKKK!!!
            expectedRideTime = self.driver.start_ride(self.rider) #def start_ride() ==> self.location = self.destination
            self.rider.updateStatus(SATISFIED)
            events.append(Dropoff(self.timestamp + expectedRideTime,self.driver,self.rider))
        elif self.rider.status == CANCELLED:
            dispatcher.activateDriver(self.driver)
            events.append(DriverRequest(self.timestamp,self.driver))
            #WHEN IS CANCEL-RIDE CALLED ? (EVENT CLASS)
        return events
    def __str__(self):
        """Return a string representation of this event.

        @type self: Pickup
        @rtype: str
        """
        return "{} -- {}: Pick up".format(self.timestamp, self.driver)


class Dropoff(Event):
    #TODO
    def __init__(self,timestamp,driver,rider):
        """Initializes a Dropoff event..

        @type self: Dropoff
        @type timestamp: int
        @type driver: Driver
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver
        self.rider = rider

    def do(self,dispatcher,monitor):
        """Carries out the dropoff event when the pickup event is called.

        @type self: Dropoff
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        >>> dispatch  = Dispatcher()
        >>> monitor = Monitor()
        >>> driver1 = Driver("driver1",Location(5,10), 10)
        >>> rider1 = Rider("rider1","waiting",Location(5,15),Location(20,5),1)
        >>> driver1.destination = rider1.destination
        >>> dropoff  = Dropoff(15,driver1,rider1)
        >>> eventList = dropoff.do(dispatch,monitor)
        >>> print(eventList[0])
        15 -- Driver: driver1, located at 5,15: Request a rider
        """
        events = []
        self.driver.end_ride()
        monitor.notify(self.timestamp,RIDER,DROPOFF,self.rider.id,self.driver.location)
        #monitor.notify(self.timestamp,DRIVER,DROPOFF,self.rider,self.driver.location)
        dispatcher.activateDriver(self.driver)#makes the driver occupied
        dispatcher.cancel_ride(self.rider)#MAkes the rider cancel the ride
        events.append(DriverRequest(self.timestamp,self.driver))

        return events
    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str
        """
        return "{} -- {}: Drop off".format(self.timestamp, self.rider)


def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]
    >>> for event in create_event_list("events.txt"): print(event)
    0 -- Driver: Amaranth, located at 1,1: Request a rider
    0 -- Driver: Bergamot, located at 1,2: Request a rider
    0 -- Driver: Crocus, located at 3,1: Request a rider
    0 -- Driver: Dahlia, located at 3,2: Request a rider
    0 -- Driver: Edelweiss, located at 4,2: Request a rider
    0 -- Driver: Foxglove, located at 5,2: Request a rider
    0 -- Almond waiting: Request a driver
    5 -- Bisque waiting: Request a driver
    10 -- Cerise waiting: Request a driver
    15 -- Desert waiting: Request a driver
    20 -- Eggshell waiting: Request a driver
    25 -- Fallow waiting: Request a driver
    """
    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]

            # HINT: Use Location.deserialize to convert the location string to
            # a location.
            event = []
            if event_type == "DriverRequest":
                # TODO
                # Create a DriverRequest event.

                driverIdentification = tokens[2]
                driverLocation = deserialize_location(tokens[3])
                driverSpeed = int(tokens[4])
                #is that all added to event?
                driver = Driver(driverIdentification,driverLocation,driverSpeed)
                events.append(DriverRequest(timestamp,driver))

            elif event_type == "RiderRequest":
                # TODO
                # Create a RiderRequest event.
                riderIdentification = tokens[2]
                riderLocation= deserialize_location(tokens[3])
                riderDestination = deserialize_location(tokens[4])
                riderPatience = int(tokens[5])
                #is that all added to event?
                rider  = Rider(riderIdentification,WAITING,riderDestination,riderLocation,riderPatience)
                events.append(RiderRequest(timestamp,rider))


    return events
