import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 


logging.info("Creating key-value input to use.")
kv_input = (pipeline | 'create i/p' >> beam.Create([('1', 'Strawberry'),
                                                    ('2', 'Carrot'),
                                                    ('3', 'Eggplant'),
                                                    ('4', 'Tomato'),
                                                    ('5', 'Potato'),]))

keys = (kv_input | 'collecting keys' >> beam.Keys() 
                 | 'keys o/p' >> beam.Map(print))


values = (kv_input | 'collecting values' >> beam.Values() 
                   | 'values o/p' >> beam.Map(print))


kvswap = (kv_input | 'swapping key-value' >> beam.KvSwap() 
                   | 'kvswap o/p' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()