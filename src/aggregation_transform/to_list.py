import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

logging.info("Conveting PCollection into list...")
input_1 = (pipeline | 'create i/p 1' >> beam.Create([1, 2, 3, 6, 44, 98])
                    | 'Count Max' >> beam.combiners.ToList()
                    | 'o/p 1' >> beam.Map(print))


dict_data_2 = (pipeline | 'create dict 2' >> beam.Create({'Sam':1, 'John':2, 'Adam':3})
                        | 'Count Dict' >> beam.combiners.ToDict()
                        | 'dict o/p 2' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()