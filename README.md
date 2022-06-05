There might be a solution with trees, I tried using trees but I could not get the time complexity right with my approach so I tried something different







# Project specification

Finish implementation of a customer events analyzer. Analyzer should store in memory two
types of entities: _customers_ and _events_ and it should provide functionality to calculate
funnel as described below (look for the TODO within the code).

## Customer

- Is identified by a string ID and they have made several events in time.
- There are multiple customers, each has only one unique ID which identifies them.

## Event

- Each event belongs to exactly one and only one customer.
- Each event happened somewhere in time (we know the unix timestamp including the decimal part) and we can assume that no two events of a single customer happened at the exact same moment.
- Each event has one string attribute called event type, which determines the type of user action.
- Examples of event types: `login`, `add_item_to_cart`, `purchase`, `subscribe_to_newsletter`.
- There is a limited number of different event types (up to 255).

The method `add_event` should store the provided event and remember it in memory in the most efficient way.

The method `calculate_funnel` should do following analysis of stored data:

- Input: Ordered sequence of event types, called steps. One event type can occur multiple times.
  - Example: `login` -> `add_item_to_cart` -> `purchase` -> `purchase` -> `logout` is a funnel with 5 steps.
- Definition: We say a customer matched the first N steps of the funnel if they had all the events in those steps and in the correct order. There can be any number of any events between two events counted as steps, it is only important that they had step 1 at some time, then step 2 at some time later, and so on. One event can only be counted towards one distinct step.

  - Example: A customer with events `A, B, A, C` matches all steps of funnels `A` (a single step funnel), `A -> B -> C` and also `A -> A`, but only matches the first step of funnel `C -> B` and only matches the first two steps of the funnel `A -> A -> B`. They match zero steps of the funnel `X -> A -> B`.

  A,B,A,C
  A,C,B

- Output: A sequence of positive integers for each step N counting the number of stored customers that matched first N steps.
  - Example: If the customer in the example above were the only customer, the result for funnel `A -> B -> C` would be `[1, 1, 1]`, whereas the result for funnel `A -> A -> B` would be `[1, 1, 0]`. Were there also another customer with events `A, C, B`, the result for `A -> B -> C` would be `[2, 2, 1]` and for `A -> A -> B` would be `[2, 1, 0]`.

The methods `add_event` and `calculate_funnel` can be called multiple times in random order (not concurrently), but generally speaking we can assume that `add_event` will be called much more often than `calculate_funnel`.
The events can arrive in any order regarding timestamp, but we can assume that it is more likely that they will arrive chronologically, but it's not guaranteed.

There is one unit test prepared. Please add more tests.

## Example usage

```
analyzer.add_event(Event("c1", "login", 1234))
analyzer.add_event(Event("c1", "purchase", 1235))
analyzer.add_event(Event("c1", "logout", 1236))
analyzer.add_event(Event("c1", "login", 1237))
analyzer.add_event(Event("c1", "purchase", 1238))
analyzer.add_event(Event("c1", "purchase", 1239))
analyzer.add_event(Event("c2", "purchase", 1235))

self.assertEqual([2, 1], analyzer.calculate_funnel(["purchase", "purchase"]))
```

`calculate_funnel` will be available from external API and called many times per second. Time complexity requirement:

- linear for `calculate_funnel`, i.e. the method should be 1000x faster for 1,000 customers than for 1,000,000 customers
- constant for `add_event`, i.e. the method should be (approximately) equally fast regardless of how many customers/events are stored

## Development

Project uses Python 3.8. The code is formatted with `black`.
