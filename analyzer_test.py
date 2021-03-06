from analyzer import Analyzer, Event, Funnel

from unittest import TestCase


class AnalyzerTest(TestCase):
    def test_simple_funnel_from_readme(self):
        analyzer = Analyzer()

        analyzer.add_event(Event("c1", "A", 1234))
        analyzer.add_event(Event("c1", "B", 1235))
        analyzer.add_event(Event("c1", "C", 1236))
        analyzer.add_event(Event("c1", "A", 1237))
        analyzer.add_event(Event("c1", "B", 1238))
        analyzer.add_event(Event("c1", "B", 1239))
        analyzer.add_event(Event("c2", "B", 1235))

        self.assertEqual([2, 1, 1],
                         analyzer.calculate_funnel(Funnel(["B", "C", "B"])))

        analyzer = Analyzer()
        analyzer.add_event(Event("c1", "A", 1234))
        analyzer.add_event(Event("c1", "B", 1235))
        analyzer.add_event(Event("c1", "A", 1236))
        analyzer.add_event(Event("c1", "C", 1237))

        self.assertEqual([1], analyzer.calculate_funnel(Funnel(["A"])))
        self.assertEqual([1, 1, 1],
                         analyzer.calculate_funnel(Funnel(["A", "B", "C"])))
        self.assertEqual([1, 1], analyzer.calculate_funnel(Funnel(["A", "A"])))
        self.assertEqual([1, 0], analyzer.calculate_funnel(Funnel(["C", "B"])))
        self.assertEqual([1, 1, 0],
                         analyzer.calculate_funnel(Funnel(["A", "A", "B"])))
        self.assertEqual([0, 0, 0],
                         analyzer.calculate_funnel(Funnel(["X", "A", "B"])))

        analyzer = Analyzer()
        analyzer.add_event(Event("c1", "A", 1234))
        analyzer.add_event(Event("c1", "B", 1235))
        analyzer.add_event(Event("c1", "A", 1236))
        analyzer.add_event(Event("c1", "C", 1237))
        analyzer.add_event(Event("c2", "A", 1237))
        analyzer.add_event(Event("c2", "C", 1237))
        analyzer.add_event(Event("c2", "B", 1237))

        self.assertEqual([2, 2, 1],
                         analyzer.calculate_funnel(Funnel(["A", "B", "C"])))
        self.assertEqual([2, 1, 0],
                         analyzer.calculate_funnel(Funnel(["A", "A", "B"])))

        analyzer = Analyzer()
        analyzer.add_event(Event("c1", "A", 1234))
        analyzer.add_event(Event("c1", "B", 1235))
        analyzer.add_event(Event("c1", "A", 1236))
        analyzer.add_event(Event("c1", "C", 1237))
        analyzer.add_event(Event("c2", "A", 1234))
        analyzer.add_event(Event("c2", "B", 1235))
        analyzer.add_event(Event("c2", "A", 1236))
        analyzer.add_event(Event("c2", "C", 1237))
        analyzer.add_event(Event("c3", "A", 1234))
        analyzer.add_event(Event("c3", "B", 1235))
        analyzer.add_event(Event("c3", "A", 1236))
        analyzer.add_event(Event("c3", "C", 1237))

        self.assertEqual([3, 3, 3],
                         analyzer.calculate_funnel(Funnel(["A", "B", "C"])))
        self.assertEqual([3, 3, 0],
                         analyzer.calculate_funnel(Funnel(["A", "A", "B"])))

    def test_simple_add_event(self):
        #Test that add_event works properly for future proof reasons
        analyzer = Analyzer()

        analyzer.add_event(Event("c1", "login", 1234))
        analyzer.add_event(Event("c1", "purchase", 1235))
        analyzer.add_event(Event("c1", "logout", 1236))
        analyzer.add_event(Event("c1", "login", 1237))
        analyzer.add_event(Event("c1", "purchase", 1238))
        analyzer.add_event(Event("c1", "purchase", 1239))
        analyzer.add_event(Event("c2", "purchase", 1235))

        self.assertEqual(analyzer.events, [{
            'customer_id': 'c1',
            'event_type': 'login',
            'timestamp': 1234
        }, {
            'customer_id': 'c1',
            'event_type': 'purchase',
            'timestamp': 1235
        }, {
            'customer_id': 'c1',
            'event_type': 'logout',
            'timestamp': 1236
        }, {
            'customer_id': 'c1',
            'event_type': 'login',
            'timestamp': 1237
        }, {
            'customer_id': 'c1',
            'event_type': 'purchase',
            'timestamp': 1238
        }, {
            'customer_id': 'c1',
            'event_type': 'purchase',
            'timestamp': 1239
        }, {
            'customer_id': 'c2',
            'event_type': 'purchase',
            'timestamp': 1235
        }])

    def test_simple_add_event_error_types(self):
        #Test that add_event will throw exceptions when missing info
        #and the type is correct

        analyzer = Analyzer()

        with self.assertRaises(Exception) as ex:
            analyzer.add_event(Event("c1", "login"))
            analyzer.add_event(Event("c1", "purchase", 1235))
        self.assertTrue(
            'missing 1 required positional argument:' in str(ex.exception))

        with self.assertRaises(Exception) as eventTypeError:
            analyzer.add_event(Event("c1", 1, 12354))
            analyzer.add_event(Event("c1", "purchase", 1235))
        self.assertTrue('Event type' in str(eventTypeError.exception))

        with self.assertRaises(Exception) as customerIdError:
            analyzer.add_event(Event(1, 1, 12354))
            analyzer.add_event(Event("c1", "purchase", 1235))
            self.assertTrue('Customer id' in str(eventTypeError.exception))

        with self.assertRaises(Exception) as timestampNegativeError:
            analyzer.add_event(Event("c1", "purchase", -1235))
        self.assertTrue('Timestamp needs to be a positive integer' in str(
            timestampNegativeError.exception))

    def test_add_event_sorted(self):
        analyzer = Analyzer()
        analyzer.add_event(Event("c1", "A", 1234))
        analyzer.add_event(Event("c1", "B", 1235))
        analyzer.add_event(Event("c1", "C", 1236))

        analyzer2 = Analyzer()
        analyzer2.add_event(Event("c1", "C", 1236))
        analyzer2.add_event(Event("c1", "B", 1235))
        analyzer2.add_event(Event("c1", "A", 1234))

        analyzer3 = Analyzer()
        analyzer3.add_event(Event("c1", "B", 1235))
        analyzer3.add_event(Event("c1", "A", 1234))
        analyzer3.add_event(Event("c1", "C", 1236))

        self.assertEqual(analyzer.events, analyzer2.events)
        self.assertEqual(analyzer2.events, analyzer3.events)
        self.assertEqual(analyzer.events, analyzer3.events)
