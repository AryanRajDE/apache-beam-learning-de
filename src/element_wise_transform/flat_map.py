import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 


def split_words(text):
    return text.split(',')

def generate_elements(elements):
    for element in elements:
        yield element

def format_plant(icon, plant):
    if icon:
        yield '{}:{}'.format(icon, plant)

def split_words_by_delimeter(text, delimiter=None):
    return text.split(delimiter)

def normalize_and_validate_durations(plant, valid_durations):
    plant['duration'] = plant['duration'].lower()
    if plant['duration'] in valid_durations:
      yield plant

def replace_duration_if_valid(plant, durations):
    if plant['duration'] in durations:
      plant['duration'] = durations[plant['duration']]
      yield plant


logging.info("FlatMap with a predefined function ...")
input_1 = (pipeline | 'create i/p 1' >> beam.Create(['Strawberry Carrot Eggplant', 'Tomato Potato'])
           | 'Split words' >> beam.FlatMap(str.split)
           | 'o/p 1' >> beam.Map(print))


logging.info("FlatMap with a user-defined function ...")
input_2 = (pipeline | 'create i/p 2' >> beam.Create(['Strawberry,Carrot,Eggplant', 'Tomato,Potato'])
           | 'Split words by udf' >> beam.FlatMap(split_words)
           | 'o/p 2' >> beam.Map(print))


logging.info("FlatMap with a lambda function ...")
input_3 = (pipeline | 'create i/p 3' >> beam.Create([['Strawberry', 'Carrot', 'Eggplant'], ['Tomato', 'Potato']])
                    | 'Flatten lists' >> beam.FlatMap(lambda elements: elements)
                    | 'o/p 3' >> beam.Map(print))


logging.info("FlatMap with a generator ...")
input_4 = (pipeline | 'create i/p 4' >> beam.Create([['Strawberry', 'Carrot', 'Eggplant'], ['Tomato', 'Potato']])
                    | 'Flatmap with generator' >> beam.FlatMap(generate_elements)
                    | 'o/p 4' >> beam.Map(print))


logging.info("FlatMapTuple with a key-value pair ...")
input_5 = (pipeline | 'create i/p 5' >> beam.Create([('1', 'Strawberry'),
                                                    ('2', 'Carrot'),
                                                    ('3', 'Eggplant'),
                                                    ('4', 'Tomato'),
                                                    ('5', 'Potato')])
                    | 'FlatMapTuple with key-value' >> beam.FlatMapTuple(format_plant)
                    | 'o/p 5' >> beam.Map(print))


logging.info("FlatMap with a multiple arguments ...")
input_6 = (pipeline | 'create i/p 6' >> beam.Create(['Strawberry,Carrot,Eggplant', 'Tomato,Potato'])
           | 'Split words by multiple args' >> beam.FlatMap(split_words_by_delimeter, delimiter=',')
           | 'o/p 6' >> beam.Map(print))


logging.info("FlatMap with a side-input singleton ...")
side_input_1 = pipeline | 'Create delimiter' >> beam.Create([','])

input_7 = (pipeline | 'create i/p 7' >> beam.Create(['Strawberry,Carrot,Eggplant', 'Tomato,Potato'])
           | 'flatmap with side i/p singleton' >> beam.FlatMap(lambda text, delimiter : text.split(delimiter),
                                                               delimiter=beam.pvalue.AsSingleton(side_input_1))
           | 'o/p 7' >> beam.Map(print))


logging.info("FlatMap with a side-input iterator ...")
side_input_2 = pipeline | 'Durations' >> beam.Create(['annual', 'biennial', 'perennial']) 

input_8 = (pipeline | 'create i/p 8' >> beam.Create([{'num': '1', 'name': 'Strawberry', 'duration': 'Perennial'},
                                                      {'num': '2', 'name': 'Carrot', 'duration': 'BIENNIAL'},
                                                      {'num': '3', 'name': 'Eggplant', 'duration': 'perennial'},
                                                      {'num': '4', 'name': 'Tomato', 'duration': 'annual'},
                                                      {'num': '5', 'name': 'Potato', 'duration': 'unknown'}])
           | 'flatmap with side i/p iterator' >> beam.FlatMap(normalize_and_validate_durations,
                                                              valid_durations=beam.pvalue.AsIter(side_input_2))
           | 'o/p 8' >> beam.Map(print))


logging.info("FlatMap with a side-input dictionary ...")
side_input_3 = pipeline | 'Durations dict' >> beam.Create([(0, 'annual'),
                                                            (1, 'biennial'),
                                                            (2, 'perennial')])

input_9 = (pipeline | 'create i/p 9' >> beam.Create([{'num': '1', 'name': 'Strawberry', 'duration': 2},
                                                      {'num': '2', 'name': 'Carrot', 'duration': 1},
                                                      {'num': '3', 'name': 'Eggplant', 'duration': 2},
                                                      {'num': '4', 'name': 'Tomato', 'duration': 0},
                                                      {'num': '5', 'name': 'Potato', 'duration': -1}])
           | 'flatmap with side i/p dictionary' >> beam.FlatMap(replace_duration_if_valid,
                                                               durations=beam.pvalue.AsDict(side_input_3))
           | 'o/p 9' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()