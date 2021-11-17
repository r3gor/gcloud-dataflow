import apache_beam
from apache_beam.io.textio import ReadFromText, WriteToText
from apache_beam.options.pipeline_options import (GoogleCloudOptions,
                                                  PipelineOptions)

from .utils import CollectTimings, CollectUsers, Split, WriteToCSV
from sys import argv

input_filename = 'gs://bi-demo-df/data.csv'
output_filename = 'gs://bi-demo-df/output'

# options = PipelineOptions()
# gcloud_options = options.view_as(GoogleCloudOptions)
# gcloud_options.job_name = 'bi-demo-job'

options = PipelineOptions(flags=argv)
gcloud_options = options.view_as(GoogleCloudOptions)

def main():
    with apache_beam.Pipeline(options=gcloud_options) as p:

        rows = (
            p |
            ReadFromText(input_filename) |
            apache_beam.ParDo(Split())
        )

        timings = (
            rows |
            apache_beam.ParDo(CollectTimings()) |
            "Grouping timings" >> apache_beam.GroupByKey() |
            "Calculating average" >> apache_beam.CombineValues(
                apache_beam.combiners.MeanCombineFn()
            )
        )

        users = (
            rows |
            apache_beam.ParDo(CollectUsers()) |
            "Grouping users" >> apache_beam.GroupByKey() |
            "Counting users" >> apache_beam.CombineValues(
                apache_beam.combiners.CountCombineFn()
            )
        )

        to_be_joined = (
            {
                'timings': timings,
                'users': users
            } |
            apache_beam.CoGroupByKey() |
            apache_beam.ParDo(WriteToCSV()) |
            WriteToText(output_filename)
        )
