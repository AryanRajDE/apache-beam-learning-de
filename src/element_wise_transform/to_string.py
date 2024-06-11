import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 


logging.info("Creating key-value pair to string ...")
"""converts a (key, value) pair into a string delimited by ','. 
   We can specify a different delimiter using the delimiter argument.
"""
input_1 = (pipeline | 'create i/p 1' >> beam.Create([('1', 'Strawberry'),
                                                    ('2', 'Carrot'),
                                                    ('3', 'Eggplant'),
                                                    ('4', 'Tomato'),
                                                    ('5', 'Potato')])
                    | 'key-value to string' >> beam.ToString.Kvs(delimiter='-')
                    | 'o/p 1' >> beam.Map(print))


logging.info("Creating elements to string ...")
"""converts an element into a string. 
   The string output will be equivalent to str(element).
"""
input_2 = (pipeline | 'create i/p 2' >> beam.Create(['1', 
                                                     'Strawberry', 
                                                     'perennial',
                                                     ['2', 'Carrot', 'biennial'],
                                                     ['3', 'Eggplant', 'perennial'],
                                                     ['4', 'Tomato', 'annual'],
                                                     ['5', 'Potato', 'perennial']])
                    | 'element to string' >> beam.ToString.Element()
                    | 'o/p 2' >> beam.Map(print))


logging.info("Creating iterables to string ...")
"""converts an iterable, in this case a list of strings, into a string delimited by ','. 
   We can specify a different delimiter using the delimiter argument. 
   The string output will be equivalent to iterable.join(delimiter).
"""
input_3 = (pipeline | 'create i/p 3' >> beam.Create([['1', 'Strawberry', 'perennial'],
                                                     ['2', 'Carrot', 'biennial'],
                                                     ['3', 'Eggplant', 'perennial'],
                                                     ['4', 'Tomato', 'annual'],
                                                     ['5', 'Potato', 'perennial']])
                    | 'iterables to string' >> beam.ToString.Iterables(delimiter=' : ')
                    | 'o/p 3' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()