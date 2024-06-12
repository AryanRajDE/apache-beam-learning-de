import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

def get_common_items(sets):
    # set.intersection() takes multiple sets as separete arguments.
    # We unpack the `sets` list into multiple arguments with the * operator.
    # The combine transform might give us an empty list of `sets`,
    # so we use a list with an empty set as a default value.
    return set.intersection(*(sets or [set()]))


input_pcoll = (pipeline | 'Create i/p 1' >> beam.Create([{'🍓', '🥕', '🍌', '🍅', '🌶️'},
                                                        {'🍇', '🥕', '🥝', '🍅', '🥔'},
                                                        {'🍉', '🥕', '🍆', '🍅', '🍍'},
                                                        {'🥑', '🥕', '🌽', '🍅', '🥥'}]))


logging.info(" Combining with a function ...")
input_1 = (input_pcoll | 'Combine with function' >> beam.CombineGlobally(get_common_items)
                       | 'o/p 1' >> beam.Map(print))


logging.info(" Combining with a lambda function ...")
input_2 = (input_pcoll 
           | 'Combine with lambda' >> beam.CombineGlobally(lambda sets: set.intersection(*(sets or [set()])))
           | 'o/p 2' >> beam.Map(print))


logging.info(" Combining with a multiple arguments ...")
input_3 = (input_pcoll 
           | 'Combine with multiple args' >> beam.CombineGlobally(lambda sets, exclude: 
                                                           set.intersection(*(sets or [set()])) - exclude,
                                                           exclude={'🥕'})
           | 'o/p 3' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()