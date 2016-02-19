from location import Location #imported for doctesting
"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:

    def __init__(self,identifier,status,destination,origin,patience):
        """Initializes the Rider class

        @type self: Rider
        @type identifier; str
        @type status: str
        @type destination: Location
        @type origin: Location
        @type patience: int
        @rtype: None
        """
        self.id = identifier
        self.status = status
        self.destination = destination #locationClass
        self.location = origin #locationClass
        self.patience = patience

    def updateStatus(self,newStatus):
        """Changes the status of the rider accordingly.

        @type self: Rider
        @type newStatus: str
        @rtype: None
        >>> rider = Rider("rider","waiting",Location(5,15),Location(20,5),100)
        >>> rider.updateStatus(CANCELLED)
        >>> print(rider.status)
        cancelled
        """
        self.status = newStatus

    def __str__(self):
        """Return a string representation.

        @type self: Rider
        @rtype: str
        >>> print(Rider("rider","waiting",Location(5,15),Location(20,5),100))
        rider waiting
        """
        return "{} {}".format(self.id,self.status)
