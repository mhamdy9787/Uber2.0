class Location:
    def __init__(self, row, column):
        """Initialize a location.

        @type self: Location
        @type row: int
        @type column: int
        @rtype: None
        """
        # TODO

        self.row = row
        self.column = column

    def __str__(self):
        """Return a string representation.

        @rtype: str
        >>> print(Location(5,10))
        5,10
        """
        # TODO
        return "{},{}".format(self.row,self.column)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @rtype: bool
        >>> location1 = Location(5,5)
        >>> location2 = Location(5,5)
        >>> location1 == location2
        True
        >>> location1 = Location(8,9)
        >>> location2 = Location(5,5)
        >>> location1 == location2
        False
        """
        # TODO
        return (self.row == other.row and self.column == other.column)


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int
    >>> origin1 = Location(6,9)
    >>> destination1 = Location(12,18)
    >>> manhattan_distance(origin1,destination1)
    15
    """
    # TODO
    return ( abs(origin.row - destination.row) + abs(origin.column - destination.column) )


def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location
    >>> location_str1 = "2,5"
    >>> print(deserialize_location(location_str1))
    2,5
    """
    # TODO
    location  = Location(int(location_str[0]),int(location_str[2]))
    return location
