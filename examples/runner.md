# How to run the beam python files

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


#### NOTE :

1. In windows, don't forget to use a backslash instead of forward slash when specifying directories.
   For example: ReadFromText('.\word_count*')
2. While using ReadFromText('.\word_count*')
   use * at the end of file which you are reading as the file contains a shard number.
