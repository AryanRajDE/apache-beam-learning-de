import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

logging.info("Counting all elements in a key-value pcollection ...")
input_1 = (pipeline | 'create i/p 1' >> beam.Create(['apple', 'ball', 'car', 'bear', 'cheetah', 'ant'])
           | 'Expression' >> beam.Map(lambda word: (word[0], word))
           | 'Count Elements' >> beam.GroupByKey()
           | 'o/p 1' >> beam.LogElements())


input_2 = (pipeline | 'Reading from file' >> beam.io.ReadFromText("src/aggreation_transform/docs/groupbykey_file.txt") 
           | 'Count Elements from file' >> beam.GroupByKey()
           | 'o/p 2' >> beam.LogElements())


input_3 = (pipeline | 'create i/p 3' >> beam.Create([('I', 1), ('You', 3), ('I', 3), ('We', 6), 
                                                     ('You', 7), ('They', 9), ('You', 5), ('They', 4)])
           | 'Count Elements from key-value pair' >> beam.GroupByKey()
           | 'o/p 3' >> beam.LogElements())


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()