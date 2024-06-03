import argparse
import apache_beam as beam 
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions

# class MyPipelineOptions(PipelineOptions):
#     @classmethod
#     def _add_argparse_args(cls, parser):
#         # setting up the custom arguments 
#         parser.add_value_provider_argument("--input", help="data input", required=True)
#         # parser.add_argument("--input", help="data input", required=True)
#         parser.add_argument("--output", help="data output", required=False)

class Split(beam.DoFn):
    def process(self, element):
        Date,Open,High,Low,Close,Volume = element.split(',')
        return [{
            'Open': str(Open),
            'Close': str(Close),
        }]

parser = argparse.ArgumentParser()

parser.add_argument("--input", default="data\SIP_DATA.txt", dest='input', help="data input")
parser.add_argument("--output", default="data\output\SIP_OUT.csv", dest='output', help="data output")

# setting up the pipeline options    
args, pipeline_args = parser.parse_known_args()
pipeline_options = PipelineOptions(pipeline_args)   
pipeline_options.view_as(SetupOptions).save_main_session = True

# defining the beam pipeline with pipeline options
pipeline = beam.Pipeline(options=pipeline_options) 

csv_lines = pipeline | beam.io.ReadFromText(args.input) 

# csv_lines| beam.Map(print)

split_columns = csv_lines | beam.ParDo(Split())

split_columns | beam.Map(print)









pipeline.run().wait_until_finish()

# for calling this file via terminal 
# python .\examples\sip_analysis.py --input="data\SIP_DATA.txt"