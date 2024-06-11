import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 







# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()