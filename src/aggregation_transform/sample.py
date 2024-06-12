import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

logging.info("Sample elements from a PCollection ...")
input_1 = (pipeline | 'create i/p 1' >> beam.Create([('spring', 2),
                                                    ('spring', 2),
                                                    ('summer', 0),
                                                    ('fall', 1),
                                                    ('spring', 2),
                                                    ('winter', 3),
                                                    ('spring', 2),
                                                    ('summer', 0),
                                                    ('fall', 1),
                                                    ('summer', 0)])
                    | 'Sample N elements' >> beam.combiners.Sample.FixedSizeGlobally(n=3)
                    | 'o/p 1' >> beam.Map(print))


logging.info("Sample elements for each key ...")
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
                    | 'Sample N elements per key' >> beam.combiners.Sample.FixedSizePerKey(n=3)
                    | 'o/p 2' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()