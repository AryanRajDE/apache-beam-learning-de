"""
    To create classic dataflow template in apache beam python
    
    While creating classic template via apache beam python you should remember to do 
    gcloud authentication via below methods.

    1. as an user - If you want your local application to temporarily use your own user credentials for API access, 
    run below command on ide terminal -
                        gcloud auth application-default login

    2. or as a service account - Try to set GOOGLE_APPLICATION_CREDENTIALS as your service account json key file 
    inside your python code. It should work.
                        os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", 
                        "path_of_project_service_account_key")

    And then only try to run the create template commands. It should work fine.

    Note : that we can not create classic template, if we choose runner=DirectRunner, as template only gets created
    when we choose the python code to be excutable via the GCP Dataflow (runner=DataflowRunner).

    Command to create classic template :
    python classic_template.py \
        --runner DataflowRunner \
        --temp_location gs://some_bucket/temp_location \
        --template_location gs://some_bucket/templates/classic_template.json \
        --save_main_session \
        --project PROJECT_ID \
        --region REGION

"""


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
        
# Create the options object
pipeline_options = PipelineOptions()
pipeline_options.view_as(SetupOptions).save_main_session = True

# Specifying that the options expected come from our custom options class
beam_options = pipeline_options.view_as(MyPipelineOptions)

# Create the pipeline - simple read/write transforms
pipeline = beam.Pipeline(options=beam_options)

lines = (pipeline 
         | 'read' >> ReadFromText(beam_options.input)
         | 'write' >> WriteToText(beam_options.output))

# running the beam pipeline
pipeline.run().wait_until_finish()
