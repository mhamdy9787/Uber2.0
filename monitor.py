

"""
The Monitor module contains the Monitor class, the Activity class,
and a collection of constants. Together the elements of the module
help keep a record of activities that have occurred.

Activities fall into two categories: Rider activities and Driver
activities. Each activity also has a description, which is one of
request, cancel, pickup, or dropoff.

=== Constants ===
@type RIDER: str
    A constant used for the Rider activity category.
@type DRIVER: str
    A constant used for the Driver activity category.
@type REQUEST: str
    A constant used for the request activity description.
@type CANCEL: str
    A constant used for the cancel activity description.
@type PICKUP: str
    A constant used for the pickup activity description.
@type DROPOFF: str
    A constant used for the dropoff activity description.
"""

RIDER = "rider"
DRIVER = "driver"

REQUEST = "request"
CANCEL = "cancel"
PICKUP = "pickup"
DROPOFF = "dropoff"


class Activity:
    """An activity that occurs in the simulation.

    === Attributes ===
    @type timestamp: int
        The time at which the activity occurred.
    @type description: str
        A description of the activity.
    @type identifier: str
        An identifier for the person doing the activity.
    @type location: Location
        The location at which the activity occurred.
    """

    def __init__(self, timestamp, description, identifier, location):
        """Initialize an Activity.

        @type self: Activity
        @type timestamp: int
        @type description: str
        @type identifier: str
        @type location: Location
        @rtype: None
        """
        self.description = description
        self.time = timestamp
        self.id = identifier
        self.location = location


class Monitor:
    """A monitor keeps a record of activities that it is notified about.
    When required, it generates a report of the activities it has recorded.
    """

    # === Private Attributes ===
    # @type _activities: dict[str, dict[str, list[Activity]]]
    #       A dictionary whose key is a category, and value is another
    #       dictionary. The key of the second dictionary is an identifier
    #       and its value is a list of Activities.

    def __init__(self):
        """Initialize a Monitor.

        @type self: Monitor
        """
        self._activities = { RIDER: {}, DRIVER: {} }
        """@type _activities: dict[str, dict[str, list[Activity]]]"""

    def __str__(self):
        """Return a string representation.

        @type self: Monitor
        @rtype: str
        """
        return "Monitor ({0} drivers, {1} riders)".format(len(self._activities[DRIVER]), len(self._activities[RIDER]))

    def notify(self, timestamp, category, description, identifier, location):
        """Notify the monitor of the activity.

        @type self: Monitor
        @type timestamp: int
            The time of the activity.
        @type category: DRIVER | RIDER
            The category for the activity.
        @type description: REQUEST | CANCEL | PICKUP | DROP_OFF
            A description of the activity.
        @type identifier: str
            The identifier for the actor.
        @type location: Location
            The location of the activity.
        @rtype: None
        """
        if identifier not in self._activities[category]:
            self._activities[category][identifier] = []

        activity = Activity(timestamp, description, identifier, location)
        self._activities[category][identifier].append(activity)

    def report(self):
        """Return a report of the activities that have occurred.

        @type self: Monitor
        @rtype: dict[str, object]
        """
        return {"rider_wait_time": self._average_wait_time(),
                "driver_total_distance": self._average_total_distance(),
                "driver_ride_distance": self._average_ride_distance()}

    def _average_wait_time(self):
        """Return the average wait time of riders that have either been picked
        up or have cancelled their ride.

        @type self: Monitor
        @rtype: float
        """
        wait_time = 0
        count = 0
        for activities in self._activities[RIDER].values():
            # A rider that has less than two activities hasn't finished
            # waiting (they haven't cancelled or been picked up).
            if len(activities) >= 2:
                # The first activity is REQUEST, and the second is PICKUP
                # or CANCEL. The wait time is the difference between the two.
                wait_time += activities[1].time - activities[0].time
                count += 1
        return wait_time / count

    def _average_total_distance(self):
        """Return the average distance drivers have driven.

        @type self: Monitor
        @rtype: float
        >>>pickup = Activity()
        >>>pickup.location.column = 5
        >>>pickup.location.row = 15
        >>>dropoff = Activity()
        >>>dropoff.location.column = 10
        >>>dropoff.location.row = 25
        >>>monitor1 = Monitor()
        >>>monitor1._activities[DRIVER].append(pickup)
        >>>monitor1._activities[DRIVER].append(dropoff)
        >>>monitor1._average_total_distance()
        15
        """
        # TODO
        distance = 0
        numberOfDriver = 0
        for activities in self._activities[DRIVER].values():#The two loops looks through all the activities for each driver
            for i in range(len(activities) -1):#Then performs a manhaatan distance on the locations of each activity
                distance += abs(activities[i].location.row - activities[i+1].location.row) + abs(activities[i].location.column - activities[i+1].location.column)
            numberOfDriver += 1
        return  distance / numberOfDriver


    def _average_ride_distance(self):
        """Return the average distance drivers have driven on rides.

        @type self: Monitor
        @rtype: float
        >>>request = Activity()
        >>>pickup = Activity()
        >>>pickup.location.column = 5
        >>>pickup.location.row = 10
        >>>dropoff = Activity()
        >>>dropoff.location.column = 20
        >>>dropoff.location.row = 15
        >>>count = 5
        >>>monitor1 = Monitor()
        >>>monitor1._activities[RIDER].append(request)
        >>>monitor1._activities[RIDER].append(pickup)
        >>>monitor1._activities[RIDER].append(dropoff)
        >>>monitor1._average_ride_distance()
        4
        """
        # TODO
        averageRideDistance = 0
        count = len(self._activities[DRIVER].values())

        for activity in self._activities[RIDER].values():
            if len(activity) == 3:#If a rider has 3 events it means they were picked up so we should find this average.
                averageRideDistance += abs( activity[1].location.row - activity[2].location.row ) + abs(activity[1].location.column - activity[2].location.column)

        return averageRideDistance / count
