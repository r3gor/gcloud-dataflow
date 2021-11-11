import apache_beam
from apache_beam.io.textio import ReadFromText, WriteToText
from apache_beam.options.pipeline_options import GoogleCloudOptions, PipelineOptions
from sys import argv

"""
Utils
"""

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


"""
Constants
"""

input_filename = 'gs://bi-demo-df/data.csv'
output_filename = 'gs://bi-demo-df/output'

options = PipelineOptions(flags=argv[1:])
gcloud_options = options.view_as(GoogleCloudOptions)

"""
Pipeline
"""

with apache_beam.Pipeline(options=gcloud_options) as p:

    rows = (
        p |
        ReadFromText(input_filename) |
        apache_beam.ParDo(Split())
    )

    timings = (
        rows |
        apache_beam.ParDo(CollectTimings()) |                   
        # (country, duration)
        # (EEUU, 0.5),
        # (EEUU, 0.5),
        # (EEUU, 1.0),
        # (UK, 3.0), ...
        
        "Grouping timings" >> apache_beam.GroupByKey() |
        # (key, value)
        # (EEUU, [0.5, 0.5, 1.0]),
        # (UK, [3.0, ...]),...

        "Calculating average" >> apache_beam.CombineValues(
            apache_beam.combiners.MeanCombineFn()
        )
        # (key, value)
        # (EEUU: 0.6666666666666666),
        # (UK: ...), ...
        
    )

    users = (
        rows |
        apache_beam.ParDo(CollectUsers()) |
        "Grouping users" >> apache_beam.GroupByKey() |
        "Counting users" >> apache_beam.CombineValues(
            apache_beam.combiners.CountCombineFn()
        )
    )

    (
        {
            'timings': timings,
            'users': users
        } |
        apache_beam.CoGroupByKey() |
        apache_beam.ParDo(WriteToCSV()) |                       # Parse to csv format
        WriteToText(output_filename, file_name_suffix='.csv')   # Write in file
    )