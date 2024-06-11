import apache_beam as beam 
import logging
import json

pipeline = beam.Pipeline() 


durations = ['annual', 'biennial', 'perennial']

def split_dataset(plant, num_partitions, ratio):
    assert num_partitions == len(ratio)
    bucket = sum(map(ord, json.dumps(plant))) % sum(ratio)
    total = 0
    for i, part in enumerate(ratio):
        total += part
        if bucket < total:
            return i
    return len(ratio) - 1


def by_duration(plant, num_partitions):
    return durations.index(plant['duration'])


logging.info("Creating common input to use.")
common_input = (pipeline | 'create common i/p' >> 
                beam.Create([{'num': '1', 'name': 'Strawberry', 'duration': 'perennial'},
                             {'num': '2', 'name': 'Carrot', 'duration': 'biennial'},
                             {'num': '3', 'name': 'Eggplant', 'duration': 'perennial'},
                             {'num': '4', 'name': 'Tomato', 'duration': 'annual'},
                             {'num': '5', 'name': 'Potato', 'duration': 'perennial'}]))


logging.info("Partition with a function ...")
annual, biennial, perennial = (common_input | 'partition by function' >> beam.Partition(by_duration, len(durations)))


logging.info("Partition with a lambda function ...")
annual, biennial, perennial = (common_input | 'partition by lambda function' >> beam.Partition(
            lambda plant, num_partitions: durations.index(plant['duration']), len(durations)))

annual | 'Annuals' >> beam.Map(lambda x: print('annual: {}'.format(x)))
biennial | 'Biennials' >> beam.Map(lambda x: print('biennial: {}'.format(x)))
perennial | 'Perennials' >> beam.Map(lambda x: print('perennial: {}'.format(x)))


logging.info("Partition with a multiple arguments ...")
train_dataset, test_dataset = (common_input | 'Partition' >> beam.Partition(split_dataset, 2, ratio=[8, 2]))

train_dataset | 'Train' >> beam.Map(lambda x: print('train: {}'.format(x)))
test_dataset | 'Test' >> beam.Map(lambda x: print('test: {}'.format(x)))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()