from event import Event, create_event_list
from container import PriorityQueue
from dispatcher import Dispatcher
from monitor import Monitor


class Simulation:
    """A simulation.
    This is the class which is responsible for setting up and running a
    simulation.
    The API is given to you: your main task is to implement the run
    method below according to its docstring.
    Of course, you may add whatever private attributes and methods you want.
    But because you should not change the interface, you may not add any public
    attributes or methods.
    This is the entry point into your program, and in particular is used for
    auto-testing purposes. This makes it ESSENTIAL that you do not change the
    interface in any way!
    """

    # === Private Attributes ===
    # @type _events: PriorityQueue[Event]
    #     A sequence of events arranged in priority determined by the event
    #     sorting order.
    # @type _dispatcher: Dispatcher
    #     The dispatcher associated with the simulation.

    def __init__(self):
        """Initialize a Simulation.
        @type self: Simulation
        @rtype: None
        """
        self._events = PriorityQueue()
        self._dispatcher = Dispatcher()
        self._monitor = Monitor()

    def run(self, initial_events):
        """Run the simulation on the list of events in <initial_events>.
        Return a dictionary containing statistics of the simulation,
        according to the specifications in the assignment handout.
        @type self: Simulation
        @type initial_events: list[Event]
            An initial list of events.
        @rtype: dict[str, object]
        """
        # TODO
        #Adding the events to the queue, UNSURE ABOUT THIS ???!??
        for event in initial_events:
            self._events.add(event)
        while not self._events.is_empty():
            currentEvent = self._events.remove()
            additionalEvents = currentEvent.do(self._dispatcher,self._monitor)
            if additionalEvents != []:
                for event in additionalEvents:
                    self._events.add(event)
        # Add all initial events to the event queue.

        # Until there are no more events, remove an event
        # from the event queue and do it. Add any returned
        # events to the event queue.

        return self._monitor.report()


if __name__ == "__main__":
    events = create_event_list("events.txt")
    sim = Simulation()
    final_stats = sim.run(events)
    print(final_stats)
