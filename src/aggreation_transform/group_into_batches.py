import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

logging.info("GroupIntoBatches to get fixed-sized batches for every key, which outputs a list of elements for every key.")
input_1 = (pipeline | 'create i/p 1' >> beam.Create([('spring', 1), 
                                                     ('spring', 3), 
                                                     ('spring', 9),
                                                     ('spring', 4), 
                                                     ('summer', 6), 
                                                     ('summer', 7), 
                                                     ('summer', 9), 
                                                     ('fall', 5), 
                                                     ('fall', 4),
                                                     ('winter', 5)])
           | 'Group elements into batch' >> beam.GroupIntoBatches(batch_size=3)
           | 'o/p 1' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()