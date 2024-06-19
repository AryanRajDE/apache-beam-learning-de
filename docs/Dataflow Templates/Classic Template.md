# Classic Templates

Classic templates package existing Dataflow pipelines to create reusable templates that you can customize for each job by changing specific pipeline parameters. Rather than writing the template, you use a command to generate the template from an existing pipeline.

The following is a brief overview of the process :

1. In your pipeline code, use the [`ValueProvider`](https://cloud.google.com/dataflow/docs/guides/templates/creating-templates#about-runtime-parameters-and-the-valueprovider-interface) interface for all pipeline options that you want to set or use at runtime. Use `DoFn` objects that accept runtime parameters.
2. Extend your template with additional metadata so that custom parameters are validated when the classic template is run. Examples of such metadata include the name of your custom classic template and optional parameters.
3. Check if the pipeline I/O connectors support `ValueProvider` objects, and make changes as required.
4. Create and stage the custom classic template.
5. Run the custom classic template.

## Required permissions for running a classic template

The permissions that you need to run the Dataflow classic template depend on where you run the template, and whether your source and sink for the pipeline are in another project.

For more information about running Dataflow pipelines either locally or by using Google Cloud, see [Dataflow security and permissions](https://cloud.google.com/dataflow/docs/concepts/security-and-permissions).

For a list of Dataflow roles and permissions, see [Dataflow access control](https://cloud.google.com/dataflow/docs/concepts/access-control).

## Limitations

* The following [pipeline option](https://cloud.google.com/dataflow/docs/reference/pipeline-options#resource_utilization) isn't supported with classic templates. If you need to control the number of worker harness threads, use [Flex Templates](https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates).

  ```
  number_of_worker_harness_threads
  ```
* The Dataflow runner doesn't support the `ValueProvider` options for Pub/Sub topics and subscription parameters. If you require Pub/Sub options in your runtime parameters, use Flex Templates.

## About runtime parameters and the `ValueProvider` **interface**

The `ValueProvider` interface allows pipelines to accept runtime parameters. Apache Beam provides three types of `ValueProvider` objects.

| Name                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RuntimeValueProvider` | `RuntimeValueProvider` is the default `ValueProvider` type. `RuntimeValueProvider` allows your pipeline to accept a value that is only available during pipeline execution. The value is not available during pipeline construction, so you can't use the value to change your pipeline's workflow graph.You can use `isAccessible()` to check if the value of a `ValueProvider` is available. If you call `get()` before pipeline execution, Apache Beam returns an error:`Value only available at runtime, but accessed from a non-runtime context.`Use `RuntimeValueProvider` when you do not know the value ahead of time. To change the parameter values at runtime, do not set values for the parameters in the template. Set the values for the parameters when you create jobs from the template. |
| `StaticValueProvider`  | `StaticValueProvider` lets you provide a static value to your pipeline. The value is available during pipeline construction, so you can use the value to change your pipeline's workflow graph.Use `StaticValueProvider` when you know the value ahead of time. See the [StaticValueProvider section](https://cloud.google.com/dataflow/docs/guides/templates/creating-templates#staticvalue) for examples.                                                                                                                                                                                                                                                                                                                                                                                                              |
| `NestedValueProvider`  | `NestedValueProvider` lets you compute a value from another `ValueProvider` object. `NestedValueProvider` wraps a `ValueProvider`, and the type of the wrapped `ValueProvider` determines whether the value is accessible during pipeline construction.Use `NestedValueProvider` when you want to use the value to compute another value at runtime. See the [NestedValueProvider section](https://cloud.google.com/dataflow/docs/guides/templates/creating-templates#nestedvalue) for examples.                                                                                                                                                                                                                                                                                                                 |

## Create and stage a classic template

After you write your pipeline, you must create and stage your template file. When you create and stage a template, the staging location contains additional files that are necessary to run your template. If you delete the staging location, the template fails to run. The Dataflow job does not run immediately after you stage the template. To run a custom template-based Dataflow job, you can use the [Google Cloud console](https://cloud.google.com/dataflow/docs/guides/templates/running-templates#custom-templates), the [Dataflow REST API](https://cloud.google.com/dataflow/docs/guides/templates/running-templates#using-the-rest-api), or the [gcloud CLI](https://cloud.google.com/dataflow/docs/guides/templates/running-templates#using-gcloud).

This Python command creates and stages a template at the Cloud Storage location specified with `--template_location`.

**Note:** If you use the Apache Beam SDK for Python 2.15.0 or later, you must specify `--region`.

```python
  python -m module_name \
    --runner DataflowRunner \
    --project PROJECT \
    --staging_location gs://staging_bucket/staging \
    --template_location gs://template_bucket/templates/ \
    --region REGION
```

After you create and stage your template, your next step is to [run the template](https://cloud.google.com/dataflow/docs/templates/running-templates).

## Running classic template

#### 1. Via REST API

To run a template with a [REST API request](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.locations.templates/launch), send an HTTP POST request with your project ID. This request requires [authorization](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.locations.templates/launch#authorization-scopes).

See the REST API reference for [projects.locations.templates.launch](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.locations.templates/launch) to learn more about the available parameters.

###### Step 1 - Create a custom template batch job

This example [projects.locations.templates.launch](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.locations.templates/launch) request creates a batch job from a template that reads a text file and writes an output text file. If the request is successful, the response body contains an instance of [LaunchTemplateResponse](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/LaunchTemplateResponse).

Modify the following values:

* Replace `<var translate="no">YOUR_PROJECT_ID</var>` with your project ID.
* Replace `<var translate="no">LOCATION</var>` with the Dataflow [region](https://cloud.google.com/dataflow/docs/resources/locations) of your choice.
* Replace `<var translate="no">JOB_NAME</var>` with a job name of your choice.
* Replace `<var translate="no">YOUR_BUCKET_NAME</var>` with the name of your Cloud Storage bucket.
* Set `gcsPath` to the Cloud Storage location of the template file.
* Set `parameters` to your list of key-value pairs.
* Set `tempLocation` to a location where you have write permission. This value is required to run Google-provided templates.

```python
POST https://dataflow.googleapis.com/v1b3/projects/YOUR_PROJECT_ID/locations/LOCATION/templates:launch?gcsPath=gs://YOUR_BUCKET_NAME/templates/TemplateName
    {
        "jobName": "JOB_NAME",
        "parameters": {
            "inputFile" : "gs://YOUR_BUCKET_NAME/input/my_input.txt",
            "output": "gs://YOUR_BUCKET_NAME/output/my_output"
        },
        "environment": {
            "tempLocation": "gs://YOUR_BUCKET_NAME/temp",
            "zone": "us-central1-f"
        }
    }
```

###### Step 2 - Use the Google API Client Libraries

Consider using the [Google API Client Libraries](https://developers.google.com/api-client-library/) to easily make calls to the Dataflow REST APIs. This sample script uses the [Google API Client Library for Python](https://developers.google.com/api-client-library/python/).

In this example, you must set the following variables:

* `project`: Set to your project ID.
* `job`: Set to a unique job name of your choice.
* `template`: Set to the Cloud Storage location of the template file.
* `parameters`: Set to a dictionary with the template parameters.

To set the [region](https://cloud.google.com/dataflow/docs/resources/locations), include the [`location`](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.locations.templates/launch#path-parameters) parameter.

```python
from googleapiclient.discovery import build

project = 'your-gcp-project'
job = 'unique-job-name'
template = 'gs://dataflow-templates/latest/Word_Count'
parameters = {
     'inputFile': 'gs://dataflow-samples/shakespeare/kinglear.txt',
     'output': 'gs://<your-gcs-bucket>/wordcount/outputs',
}

dataflow = build("dataflow", "v1b3")
request = (
    dataflow.projects()
    .templates()
    .launch(
        projectId=project,
        gcsPath=template,
        body={
            "jobName": job,
            "parameters": parameters,
        },
    )
)

response = request.execute()
```

For more information about the available options, see the [`projects.locations.templates.launch` method](https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.locations.templates/launch) in the Dataflow REST API reference.

#### 2. Via gcloud CLI

The gcloud CLI can run either a custom or a [Google-provided](https://cloud.google.com/dataflow/docs/templates/provided-templates) template using the `gcloud dataflow jobs run` command. Examples of running Google-provided templates are documented in the [Google-provided templates page](https://cloud.google.com/dataflow/docs/templates/provided-templates).

For the following custom template examples, set the following values:

* Replace `<var translate="no">JOB_NAME</var>` with a job name of your choice.
* Replace `<var translate="no">YOUR_BUCKET_NAME</var>` with the name of your Cloud Storage bucket.
* Set `--gcs-location` to the Cloud Storage location of the template file.
* Set `--parameters` to the comma-separated list of parameters to pass to the job. Spaces between commas and values are not allowed.
* To prevent VMs from accepting SSH keys that are stored in project metadata, use the `additional-experiments` flag with the [`block_project_ssh_keys`](https://cloud.google.com/dataflow/docs/reference/service-options) service option: `--additional-experiments=block_project_ssh_keys`.

###### Step 1- Create and run custom template batch job

This example creates a batch job from a template that reads a text file and writes an output text file.

```python
gcloud dataflow jobs run JOB_NAME \
--gcs-location gs://YOUR_BUCKET_NAME/templates/MyTemplate \
--parameters inputFile=gs://YOUR_BUCKET_NAME/input/my_input.txt,output=gs://YOUR_BUCKET_NAME/output/my_output

The request returns a response with the following format :-
    id: 2016-10-11_17_10_59-1234530157620696789
    projectId: YOUR_PROJECT_ID
    type: JOB_TYPE_BATCH
```

## References and Links

1. [Create Classic Dataflow Templates](https://cloud.google.com/dataflow/docs/guides/templates/creating-templates)
2. [Running Classic Templates](https://cloud.google.com/dataflow/docs/guides/templates/running-templates)
