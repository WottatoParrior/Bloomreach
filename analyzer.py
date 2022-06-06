from typing import List

# eg : customers = { 1 : [1,2,3,4] , 2 : [5,6] , 7 : [9,10]}


class Event:
    def __init__(self, customer_id: str, event_type: str, timestamp: float):
        self.customer_id = customer_id
        self.event_type = event_type
        self.timestamp = timestamp


class Funnel:
    def __init__(self, steps: List[str]):
        self._steps = steps


class Analyzer:
    def __init__(self):
        self.events: List[Event] = []
        self.customers = {}
        self.combinedEvents: List[str] = []
        pass

    def add_event(self, event: Event):

        if type(event.customer_id) is not str:
            raise Exception("Customer id needs to be string")
        if type(event.event_type) is not str:
            raise Exception("Event type needs to be string")
        if type(event.timestamp) is not int or event.timestamp < 0:
            raise Exception("Timestamp needs to be a positive integer")
        # If there are no events just append the first one
        if len(self.events) == 0:
            self.events.append({
                "customer_id": event.customer_id,
                "event_type": event.event_type,
                "timestamp": event.timestamp
            })
        # Else iterate over the events and if the incoming event is older than
        # the current one, place it before it
        # Also make sure that the event belongs to the correct customer or there might be issues
        else:

            for idx in range(0, len(self.events)):
                if self.events[idx][
                        "timestamp"] > event.timestamp and self.events[idx][
                            "customer_id"] == event.customer_id:
                    self.events.insert(
                        idx, {
                            "customer_id": event.customer_id,
                            "event_type": event.event_type,
                            "timestamp": event.timestamp
                        })
                    break
                elif idx == (len(self.events) - 1):
                    self.events.append({
                        "customer_id": event.customer_id,
                        "event_type": event.event_type,
                        "timestamp": event.timestamp
                    })
        pass

    def cleanPlace(self):
        self.events = []
        self.customers = {}
        self.combinedEvents = []

    def createCustomers(self):
        for event in self.events:
            cid = event["customer_id"]
            event_type = event["event_type"]
            if (cid in self.customers):
                self.customers[cid].append(event_type)
            else:
                self.customers[cid] = [event_type]

    def createCombinedEventsList(self):
        for _, value in self.customers.items():
            self.combinedEvents.extend(value)
            self.combinedEvents.append("CustomerChange")
        self.combinedEvents.pop()

    def calculate_funnel(self, funnel: Funnel) -> List[int]:
        # Create the initial values for the output [0,0,0,0.....]
        values = [0] * len(funnel._steps)

        # Initialize the customers information
        if len(self.customers) == 0:
            self.createCustomers()

        # This is were things become interesting
        # My purpose is to create an array like this [A,B,B,B,CustomerChange,B,C,A,B,CustomerChange,B,A,A......]
        # This is representation is an idea from tree representations and traversals
        # What I am doing is create a dictionary with info for each customer
        # When I match the step with the event I store in the dictionary the index where the match happened
        # and also the current iteration of the funnel step.

        # Example: funnel_step 1 is 'A', my initial customer number is 1,
        # when I traverse the array [A,B,B,B,CustomerChange,B,C,A,B...] I find A in index 0,
        # I increase the value[0] since funnel_step 1 corresponds to value[0] in [0,0,0]
        # and the dictionary becomes  {1 : lastIndex : 0, funnelStep : 1}
        # now for the next values B,B,B there wont be any check for customer 1 since the funnelStep info
        # has already been updated. After I encounter CustomerChange, I increment the customerNumber
        # so the only values that will be updated now will be for customer 2 etc etc
        # There is the danger that I match the indexo 0 again when i repeat the process for funnel_step 2
        # so in order to bypass that I keep the lastIndex entry in dictionary. This entry remembers where the last
        # match happened so we dont match again by accident

        if len(self.combinedEvents) == 0:
            self.createCombinedEventsList()

        # Create dictionary entries for the amount of different customers
        noOfDifferentCustomers = self.combinedEvents.count(
            "CustomerChange") + 1
        helpDict = {}

        for helper in range(1, noOfDifferentCustomers + 1):
            helpDict[helper] = {"lastIndex": 0, "funnelStep": 0}
        i = 0

        # This is linear in regards to customers, no matter how many customers we have,
        # the time complexity increases linearly.

        for step in funnel._steps:
            customerNumber = 1
            for idx, event in enumerate(self.combinedEvents):

                if (event == step) and (
                        helpDict[customerNumber]["funnelStep"] == i) and (
                            idx >= helpDict[customerNumber]["lastIndex"]):
                    values[i] += 1
                    helpDict[customerNumber]["lastIndex"] = idx + 1
                    helpDict[customerNumber]["funnelStep"] += 1

                if event == "CustomerChange":
                    customerNumber += 1

            i += 1

        return values
