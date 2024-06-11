import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

logging.info("Merging different pcollection via Flatten ...")
"""Merges multiple PCollection objects into a single logical PCollection. 
   A transform for PCollection objects that store the same data type.
"""

wordsStartingWithA = pipeline | 'Words starting with A' >> beam.Create(['apple', 'ant', 'arrow'])
  
wordsStartingWithB = pipeline | 'Words starting with B' >> beam.Create(['ball', 'book', 'bow'])

flattening = ((wordsStartingWithA, wordsStartingWithB) 
              | beam.Flatten()
              | beam.LogElements())


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()