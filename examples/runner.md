# How To Run

This runner file contains the details on how to run the beam files with python codes and also how to run the beam templates on the cloud dataflow.

### To Run the Python Files

#### DirectRunner

```python
python -m word_count_minimal --input .\data\inputs\word_count* --output .\data\outputs\counts --runner DirectRunner
```

#### DataflowRunner

```python
python -m word_count_minimal --input .\data\inputs\word_count* 
			     --output .\data\outputs\counts
                             --runner DataflowRunner
			     --project YOUR_GCP_PROJECT
    			     --region YOUR_GCP_REGION
    			     --temp_location gs://YOUR_GCS_BUCKET/tmp/
```

### To Run the Beam Templates

##### Template Parameters

| Parameter     | Description                                      |
| ------------- | ------------------------------------------------ |
| `inputFile` | The Cloud Storage input file's path.             |
| `output`    | The Cloud Storage output file's path and prefix. |

##### **1. via gcloud**

In your shell or terminal, run the template:

```shell
gcloud dataflow jobs run JOB_NAME \\
    --gcs-location gs://dataflow-templates/latest/Word_Count \\
    --region REGION_NAME \\
    --parameters \\
    inputFile=gs://dataflow-samples/shakespeare/kinglear.txt,\\
    output=gs://BUCKET_NAME/output/my_output
```

Replace the following:

* `JOB_NAME`: a unique job name of your choice
* `REGION_NAME`: the [region](https://cloud.google.com/dataflow/docs/resources/locations) where you want to deploy your Dataflow job—for example, `us-central1`
* `BUCKET_NAME`: the name of your Cloud Storage bucket

##### 2. via api

To run the template using the REST API, send an HTTP POST request. For more information on the API and its authorization scopes, see [`projects.templates.launch`](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.templates/launch).

```python
POST https://dataflow.googleapis.com/v1b3/projects/PROJECT_ID/locations/LOCATION/templates:launch?gcsPath=gs://dataflow-templates/latest/Word_Count
{
    "jobName":"JOB_NAME",
    "parameters":{
       "inputFile":"gs://dataflow-samples/shakespeare/kinglear.txt",
       "output":"gs://BUCKET_NAME/output/my_output"
    },
    "environment":{"zone":"us-central1-f"}
}
```

Replace the following:

* `PROJECT_ID`: the Google Cloud project ID where you want to run the Dataflow job
* `JOB_NAME`: a unique job name of your choice
* `LOCATION`: the [region](https://cloud.google.com/dataflow/docs/resources/locations) where you want to deploy your Dataflow job—for example, `us-central1`
* `BUCKET_NAME`: the name of your Cloud Storage bucket


### What to do for creating templates

There's one primary change in the code when you want to create a beam template i.e., the change of your args given to the pipeline.

For example, an **ordinary pipeline** will run with normal parser args such as:

```python
def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',
                        default='gs://path/to/input.txt',
                        help='input text file')
    parser.add_argument('--output',
                        default='gs://path/to/output.txt',
                        help='output text file')

    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)

    p = beam.Pipeline(options=pipeline_options)
```



Now for a **templatable pipeline**, all you need to do is make a class for your args, change `add_argument` to  `add_value_provider_argument` , and finally make the options accessible in as an object.

```python
class ContactUploadOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument(
            '--path',
            type=str,
            help='path of input file')
        parser.add_value_provider_argument(
            '--source',
            type=str,
            help='source name')

def run():
    contact_options = PipelineOptions().view_as(ContactUploadOptions)
    pipeline_options = PipelineOptions()
  
    p = beam.Pipeline(options=pipeline_options)
```


#### NOTE

1. In windows, don't forget to use a backslash instead of forward slash when specifying directories.
   For example: ReadFromText('.\word_count*')
2. While using ReadFromText('.\word_count*')
   use * at the end of file which you are reading as the file contains a shard number.
