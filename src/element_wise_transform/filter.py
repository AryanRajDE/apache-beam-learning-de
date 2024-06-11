import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

# functions used in below cases 
def is_perennial(plant):
    return plant['duration'] == 'perennial'

def has_duration(plant, duration):
    return plant['duration'] == duration


logging.info("Creating common input to use.")
common_input = (pipeline | 'create common i/p' >> 
                beam.Create([{'num': '1', 'name': 'Strawberry', 'duration': 'perennial'},
                             {'num': '2', 'name': 'Carrot', 'duration': 'biennial'},
                             {'num': '3', 'name': 'Eggplant', 'duration': 'perennial'},
                             {'num': '4', 'name': 'Tomato', 'duration': 'annual'},
                             {'num': '5', 'name': 'Potato', 'duration': 'perennial'}]))

logging.info("Filter with a function ...")
input_1 = (common_input | 'filtering by function' >> beam.Filter(is_perennial)
                        | 'o/p 1' >> beam.Map(print))


logging.info("Filter with a lambda function ...")
input_2 = (common_input 
           | 'filtering by lambda' >> beam.Filter(lambda data : data['duration'] == 'perennial')
           | 'o/p 2' >> beam.Map(print))


logging.info("Filter with a multiple argument function ...")
input_3 = (common_input
           | 'filtering by multiple args' >> beam.Filter(has_duration, duration='annual')
           | 'o/p 3' >> beam.Map(print))


logging.info("Filter with side-input as singleton ...")
side_input_1 = pipeline | 'Perennial' >> beam.Create(['perennial'])

input_4 = (common_input
           | 'filtering by side i/p singleton' >> beam.Filter(lambda data, duration : data['duration']==duration,
                                                              duration=beam.pvalue.AsSingleton(side_input_1))
           | 'o/p 4' >> beam.Map(print))


logging.info("Filter with side-input as iterator ...")
side_input_2 = pipeline | 'valid duration' >> beam.Create(['annual', 'biennial'])

input_5 = (common_input
           | 'filtering by side i/p iterator' >> beam.Filter(lambda data, val_duration : data['duration'] in val_duration,
                                                             val_duration=beam.pvalue.AsIter(side_input_2))
           | 'o/p 5' >> beam.Map(print))


logging.info("Filter with side-input as dictionary ...")
side_input_3 = pipeline | 'keep duration' >> beam.Create([('annual', False),
                                                          ('biennial', False),
                                                          ('perennial', True)])

input_6 = (common_input
           | 'filtering by side i/p dictionary' >> beam.Filter(lambda data, keep_duration : keep_duration[data['duration']],
                                                               keep_duration=beam.pvalue.AsDict(side_input_3))
           | 'o/p 6' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()