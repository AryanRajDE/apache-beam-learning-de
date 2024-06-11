import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 


logging.info("MapTuple for key:value pairs ...")
input_1 = (pipeline | 'create i/p 1' >> beam.Create([('1', 'Strawberry'),
                                                     ('2', 'Carrot'),
                                                     ('3', 'Eggplant'),
                                                     ('4', 'Tomato'),
                                                     ('5', 'Potato')])
                    | 'format by map-tuple' >> beam.MapTuple(lambda num, plant : '{}-{}'.format(num, plant))
                    | 'o/p 1' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()