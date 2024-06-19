import os
import apache_beam as beam
from apache_beam.io import ReadFromText, WriteToText
from apache_beam.options.pipeline_options import SetupOptions, PipelineOptions

os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", 
                      "path_of_project_service_account_key")

class MyPipelineOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        # Use add_value_provider_argument for arguments to be templatable
        # Use add_argument as usual for non-templatable arguments

        parser.add_value_provider_argument('--input',
                                           type=str,
                                           help='Path of the file to read from')
        
        parser.add_value_provider_argument('--output',
                                           type=str,
                                           help='Output file to write results to.')
        
# Create the options object via SetupOptions
pipeline_options = PipelineOptions()
pipeline_options.view_as(SetupOptions).save_main_session = True

# Specifying that the options expected come from our custom options class
beam_options = pipeline_options.view_as(MyPipelineOptions)

# Create the pipeline - simple read/write transforms
pipeline = beam.Pipeline(options=beam_options)

lines = (pipeline 
         | 'read' >> ReadFromText(beam_options.input)
         | 'write' >> WriteToText(beam_options.output, num_shards=1, shard_name_template=''))

# running the beam pipeline
pipeline.run().wait_until_finish()
