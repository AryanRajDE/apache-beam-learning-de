# Create classic dataflow template in apache beam python

While creating classic template via apache beam python you should remember to do `gcloud authentication` via one of the given methods.

1. `as a user` - If you want your local application to temporarily use your own user credentials for API access. Run below command on ide terminal -

   ```python
   gcloud auth application-default login
   ```
2. `as a service account` - Try to set **GOOGLE_APPLICATION_CREDENTIALS** as your service account json key file inside your python code. It should work.

   ```python
   os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "path_of_project_service_account_key")
   ```

And then only try to run the create template commands. It should work fine.

**Note :** 

* We can not create classic template, if we choose runner=DirectRunner, as template only gets created when we choose the python code to be excutable via the GCP Dataflow (runner=DataflowRunner).
* Check `classic_template.py` code files given inside ClassicTemplate directory to understand how to create the classic template and how to run those template on gcp dataflow.
* Check `dataflow_runner.ipynb` notebook given inside ClassicTemplate directory to understand how to run the classic template using `REST API` or `gcloud commands`.

### **Command to create classic template** 

```python
python classic_template.py \
        --runner DataflowRunner \
        --temp_location gs://some_bucket/temp_location \
        --template_location gs://some_bucket/templates/classic_template.json \
        --save_main_session \
        --project PROJECT_ID \
        --region REGION
```

### Command to run classic template

```pyrhon
gcloud dataflow jobs run test-classic-job \
--project projectId \
--gcs-location gs://your_classic_template_bucket_file_location/template.json \
--region us-central1 \
--service-account-email your_service_account_name \
--staging-location gs://your_staging_bucket_location \
--subnetwork your_full_subnetwork_url \
--num-workers 4 \
--max-workers 8 \
--disable-public-ips \
--worker-region us-central1 \
--worker-machine c2-standard-8 \
--parameters input=gs://your_runtime_value_provider_input_value,output=gs://your_runtime_value_provider_output_value
```
