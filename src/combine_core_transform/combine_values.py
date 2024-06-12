import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

def saturated_sum(values):
    max_value = 8
    return min(sum(values), max_value)

logging.info(" Combining with a pre-defined function pdf ...")
input_1 = (pipeline | 'Create i/p 1' >> beam.Create([('🥕', [3, 2]),
                                                     ('🍆', [1]),
                                                     ('🍅', [4, 5, 3])])
                    | 'Combine with pdf' >> beam.CombineValues(sum)
                    | 'o/p 1' >> beam.Map(print))


logging.info(" Combining with a user-defined function udf ...")
input_2 = (pipeline | 'Create i/p 2' >> beam.Create([('🥕', [3, 2]),
                                                     ('🍆', [1]),
                                                     ('🍅', [4, 5, 3])])
                    | 'Combine with udf' >> beam.CombineValues(saturated_sum)
                    | 'o/p 2' >> beam.Map(print))


logging.info(" Combining with a lambda function ...")
input_3 = (pipeline | 'Create i/p 3' >> beam.Create([('🥕', [3, 2]),
                                                     ('🍆', [1]),
                                                     ('🍅', [4, 5, 3])])
                    | 'Combine with lambda' >> beam.CombineValues(lambda element: min(sum(element), 8))
                    | 'o/p 3' >> beam.Map(print))


logging.info(" Combining with multiple arguments ...")
input_4 = (pipeline | 'Create i/p 4' >> beam.Create([('🥕', [3, 2]),
                                                     ('🍆', [1]),
                                                     ('🍅', [4, 5, 3])])
    | 'Combine with multiple args' >> beam.CombineValues(lambda element, max_value: 
                                                         min(sum(element), max_value), max_value=8)
    | 'o/p 4' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()