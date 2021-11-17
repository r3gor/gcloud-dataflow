import apache_beam

class Split(apache_beam.DoFn):

    def process(self, element):
        country, duration, user = element.split(",")

        return [{
            'country': country,
            'duration': float(duration),
            'user': user
        }]

class CollectTimings(apache_beam.DoFn):

    def process(self, element):
        """
        Returns a list of tuples containing country and duration
        """

        result = [
            (element['country'], element['duration'])
        ]
        return result


class CollectUsers(apache_beam.DoFn):

    def process(self, element):
        """
        Returns a list of tuples containing country and user name
        """
        result = [
            (element['country'], element['user'])
        ]
        return result


class WriteToCSV(apache_beam.DoFn):

    def process(self, element):
        """
        Prepares each row to be written in the csv
        """
        result = [
            "{},{},{}".format(
                element[0],
                element[1]['users'][0],
                element[1]['timings'][0]
            )
        ]
        return result