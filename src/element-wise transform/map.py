import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

# functions used in below cases 
def count_length(text):
    return len(text)

def replace_char(text, old_char=None, new_char=None):
    if old_char in text:
        return text.replace(old_char, new_char)
    else:
        return "Nothing to replace ..."
    
def replace_duration(plant, durations):
    plant['duration'] = durations[plant['duration']]
    return plant


logging.info("Map with a pre-defined function ...")
input_1 = (pipeline | 'create i/p 1' >> beam.Create(['Strawberry \n', 'Carrot \n', 'Eggplant \n',
                                                'Tomato \n', 'Potato \n'])
                                                
                    | 'Strip' >> beam.Map(str.strip)
                    | 'o/p 1' >> beam.Map(print))


logging.info("Map with a user-defined function ...")
input_2 = (pipeline | 'create i/p 2' >> beam.Create(['Strawberry', 'Carrot', 'Eggplant',
                                                        'Tomato', 'Potato'])
                    | 'map by udf' >> beam.Map(count_length)
                    | 'o/p 2' >> beam.Map(print))


logging.info("Map with a lambda function ...")
input_3 = (pipeline | 'create i/p 3' >> beam.Create(['Strawberry', 'Carrot', 'Eggplant', 'Tomato', 'Potato'])
                    | 'map by lambda' >> beam.Map(lambda text : len(text)) 
                    | 'o/p 3' >> beam.Map(print))


logging.info("Map with multiple arguments ...")
input_4 = (pipeline | 'create i/p 4' >> beam.Create(['Strawberry', 'Carrot', 'Eggplant', 'Tomato', 'Potato']) 
                    | 'map by multiple args' >> beam.Map(replace_char, old_char='r' , new_char='xxx')
                    | 'o/p 4' >> beam.Map(print))


logging.info("Map with side-input as singleton ...")
side_input_1 =  pipeline | 'create side i/p 1' >> beam.Create(['***'])

input_5 = (pipeline | 'create i/p 5' >> beam.Create(['Strawberry', 'Carrot', 'Eggplant', 'Tomato', 'Potato']) 
                    | 'map by side i/p singleton' >> beam.Map(lambda text, char: text.replace('r', char),
                                                              char=beam.pvalue.AsSingleton(side_input_1))
                    | 'o/p 5' >> beam.Map(print))


logging.info("Map with side-input as iterator or as list...")
side_input_2 =  pipeline | 'create side i/p 2' >> beam.Create(['*', '#', '$'])

input_6 = (pipeline | 'create i/p 6' >> beam.Create(['Strawberry', 'Carrot', 'Eggplant', 'Tomato', 'Potato']) 
                    | 'map by side i/p iterator' >> beam.Map(lambda text, char: text.replace('r', ''.join(char)),
                                                              char=beam.pvalue.AsIter(side_input_2))                     
                    | 'o/p 6' >> beam.Map(print))

input_7 = (pipeline | 'create i/p 7' >> beam.Create(['Strawberry', 'Carrot', 'Eggplant', 'Tomato', 'Potato']) 
                    | 'map by side i/p list' >> beam.Map(lambda text, char: text.replace('r', ''.join(char)),
                                                              char=beam.pvalue.AsList(side_input_2))                            
                    | 'o/p 7' >> beam.Map(print))


logging.info("Map with side-input as dictionaries...")
side_input_3 = pipeline | 'Durations' >> beam.Create([(0, 'annual'),
                                                      (1, 'biennial'),
                                                      (2, 'perennial')])

input_8 =  (pipeline | 'create i/p 8' >> beam.Create([{'num': '1', 'name': 'Strawberry', 'duration': 2},
                                                      {'num': '2', 'name': 'Carrot', 'duration': 1},
                                                      {'num': '3', 'name': 'Eggplant', 'duration': 2},
                                                      {'num': '4', 'name': 'Tomato', 'duration': 0},
                                                      {'num': '5', 'name': 'Potato', 'duration': 2}])
                    | 'map by side i/p dict' >> beam.Map(replace_duration,
                                                        durations=beam.pvalue.AsDict(side_input_3))
                    | 'o/p 8' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()