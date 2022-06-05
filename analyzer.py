from ast import Or
from opcode import HAVE_ARGUMENT
from pickle import FALSE
from pydoc import doc
from typing import List, Dict
from collections import defaultdict

from numpy import number
import json
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

        if len(self.events) == 0:
            self.events.append({
                "customer_id": event.customer_id,
                "event_type": event.event_type,
                "timestamp": event.timestamp
            })
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
        values = [0] * len(funnel._steps)

        if len(self.customers) == 0:
            self.createCustomers()

        if len(self.combinedEvents) == 0:
            self.createCombinedEventsList()

        noOfDifferentCustomers = self.combinedEvents.count(
            "CustomerChange") + 1
        helpDict = {}

        for helper in range(1, noOfDifferentCustomers + 1):
            helpDict[helper] = {"lastIndex": 0, "funnelStep": 0}
        i = 0
        # print("Funnel steps are", funnel._steps)
        # print("Combined events are", self.combinedEvents)
        # This is linear in regards to customers, no matter how many customers we have
        # the time complexity remains linear

        for step in funnel._steps:
            eventIndex = 0
            customerNumber = 1
            for event in range(0, len(self.combinedEvents)):
                # print("Iteration is", i, "Dict is ", helpDict,
                #       "Event Index is", eventIndex, "Step is", step,
                #       "Event is", self.combinedEvents[event], "Values are",
                #       values, "Customer Number is", customerNumber)

                if (self.combinedEvents[event] == step
                    ) and (helpDict[customerNumber]["funnelStep"] == i) and (
                        eventIndex >= helpDict[customerNumber]["lastIndex"]):
                    values[i] += 1
                    helpDict[customerNumber]["lastIndex"] = eventIndex + 1
                    helpDict[customerNumber]["funnelStep"] += 1

                if self.combinedEvents[event] == "CustomerChange":
                    customerNumber += 1

                eventIndex += 1
            i += 1
        # print("Final values are", values)

        return values
