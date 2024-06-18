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

| Name                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `RuntimeValueProvider` | `RuntimeValueProvider` is the default `ValueProvider` type. `RuntimeValueProvider` allows your pipeline to accept a value that is only available during pipeline execution. The value is not available during pipeline construction, so you can't use the value to change your pipeline's workflow graph.You can use `isAccessible()` to check if the value of a `ValueProvider` is available. If you call `get()` before pipeline execution, Apache Beam returns an error:`Value only available at runtime, but accessed from a non-runtime context.`Use `RuntimeValueProvider` when you do not know the value ahead of time. To change the parameter values at runtime, do not set values for the parameters in the template. Set the values for the parameters when you create jobs from the template. |
| `StaticValueProvider`  | `StaticValueProvider` lets you provide a static value to your pipeline. The value is available during pipeline construction, so you can use the value to change your pipeline's workflow graph.Use `StaticValueProvider` when you know the value ahead of time. See the [StaticValueProvider section](https://cloud.google.com/dataflow/docs/guides/templates/creating-templates#staticvalue) for examples.                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `NestedValueProvider`  | `NestedValueProvider` lets you compute a value from another `ValueProvider` object. `NestedValueProvider` wraps a `ValueProvider`, and the type of the wrapped `ValueProvider` determines whether the value is accessible during pipeline construction.Use `NestedValueProvider` when you want to use the value to compute another value at runtime. See the [NestedValueProvider section](https://cloud.google.com/dataflow/docs/guides/templates/creating-templates#nestedvalue) for examples.                                                                                                                                                                                                                                                                                                                      |


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


## References and Links

1. [Create Classic Dataflow Templates](https://cloud.google.com/dataflow/docs/guides/templates/creating-templates)
2. [Running Classic Templates](https://cloud.google.com/dataflow/docs/guides/templates/running-templates)
