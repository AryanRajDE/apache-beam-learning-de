import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

logging.info("Maximum element in a PCollection ...")
input_1 = (pipeline | 'create i/p 1' >> beam.Create([1, 2, 3, 6, 44, 98])
                    | 'Count Max' >> beam.CombineGlobally(lambda elements: max(elements or [None]))
                    | 'o/p 1' >> beam.Map(print))


logging.info("Maximum elements for each key ...")
input_2 = (pipeline | 'create i/p 2' >> beam.Create([('spring', 2),
                                                    ('spring', 2),
                                                    ('summer', 0),
                                                    ('fall', 1),
                                                    ('spring', 6),
                                                    ('winter', 3),
                                                    ('spring', 2),
                                                    ('summer', 4),
                                                    ('fall', 1),
                                                    ('summer', 0)])
           | 'Count Max per Key' >> beam.CombinePerKey(max)
           | 'o/p 2' >> beam.Map(print))


logging.info("Mean of element in a PCollection ...")
input_3 = (pipeline | 'create i/p 3' >> beam.Create([1, 2, 3, 6, 44, 98])
                    | 'Count Mean' >> beam.combiners.Mean.Globally()
                    | 'o/p 3' >> beam.Map(print))


logging.info("Mean of elements for each key ...")
input_4 = (pipeline | 'create i/p 4' >> beam.Create([('spring', 2),
                                                    ('spring', 2),
                                                    ('summer', 0),
                                                    ('fall', 1),
                                                    ('spring', 6),
                                                    ('winter', 3),
                                                    ('spring', 2),
                                                    ('summer', 4),
                                                    ('fall', 1),
                                                    ('summer', 0)])
           | 'Count Mean per Key' >> beam.combiners.Mean.PerKey()
           | 'o/p 4' >> beam.Map(print))


logging.info("Minimum element in a PCollection ...")
input_5 = (pipeline | 'create i/p 5' >> beam.Create([1, 2, 3, 6, 44, 98])
                    | 'Count Min' >> beam.CombineGlobally(lambda elements: min(elements or [-1]))
                    | 'o/p 5' >> beam.Map(print))


logging.info("Minimum elements for each key ...")
input_6 = (pipeline | 'create i/p 6' >> beam.Create([('spring', 2),
                                                    ('spring', 2),
                                                    ('summer', 0),
                                                    ('fall', 1),
                                                    ('spring', 6),
                                                    ('winter', 3),
                                                    ('spring', 2),
                                                    ('summer', 4),
                                                    ('fall', 1),
                                                    ('summer', 0)])
           | 'Count Min per Key' >> beam.CombinePerKey(min)
           | 'o/p 6' >> beam.Map(print))


logging.info("Sum of element in a PCollection ...")
input_7 = (pipeline | 'create i/p 7' >> beam.Create([1, 2, 3, 6, 44, 98])
                    | 'Count Sum' >> beam.CombineGlobally(sum)
                    | 'o/p 7' >> beam.Map(print))


logging.info("Sum of elements for each key ...")
input_8 = (pipeline | 'create i/p 8' >> beam.Create([('spring', 2),
                                                    ('spring', 2),
                                                    ('summer', 0),
                                                    ('fall', 1),
                                                    ('spring', 6),
                                                    ('winter', 3),
                                                    ('spring', 2),
                                                    ('summer', 4),
                                                    ('fall', 1),
                                                    ('summer', 0)])
           | 'Count Sum per Key' >> beam.CombinePerKey(sum)
           | 'o/p 8' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()