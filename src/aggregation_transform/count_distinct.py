import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

logging.info("Counting all elements in a pcollection ...")
input_1 = (pipeline | 'create i/p 1' >> beam.Create([1, 2, 3, 6, 44, 98])
           | 'Count Elements' >> beam.combiners.Count.Globally()
           | 'o/p 1' >> beam.Map(print))


logging.info("Counting all elements per key in a pcollection ...")
input_2 = (pipeline | 'create i/p 2' >> beam.Create([('spring', 2),
                                                    ('spring', 2),
                                                    ('summer', 0),
                                                    ('fall', 1),
                                                    ('spring', 2),
                                                    ('winter', 3),
                                                    ('spring', 2),
                                                    ('summer', 0),
                                                    ('fall', 1),
                                                    ('summer', 0)])
           | 'Count Elements per Key' >> beam.combiners.Count.PerKey()
           | 'o/p 2' >> beam.Map(print))


logging.info("Counting all unique elements in a pcollection ...")
input_3 = (pipeline | 'create i/p 3' >> beam.Create([1, 2, 3, 6, 3, 1, 66, 2, 44, 98])
           | 'Count Unique Elements' >> beam.combiners.Count.PerElement()
           | 'o/p 3' >> beam.Map(print))


logging.info("Counting all unique elements in a pcollection ...")
input_4 = (pipeline | 'create i/p 4' >> beam.Create([1, 2, 3, 6, 3, 1, 66, 2, 44, 98])
           | 'Count Distinct Elements' >> beam.Distinct()
           | 'o/p 4' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()