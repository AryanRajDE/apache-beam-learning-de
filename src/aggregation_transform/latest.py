import apache_beam as beam 
import logging
import time

pipeline = beam.Pipeline() 

def to_unix_time(time_str, format='%Y-%m-%d %H:%M:%S'):
    return time.mktime(time.strptime(time_str, format))

logging.info("Latest element globally ...")
input_1 = (pipeline | 'create i/p 1' >> beam.Create([{'item': '🥬', 'harvest': '2020-02-24 00:00:00'},
                                                    {'item': '🍓', 'harvest': '2020-06-16 00:00:00'},
                                                    {'item': '🥕', 'harvest': '2020-07-17 00:00:00'},
                                                    {'item': '🍆', 'harvest': '2020-10-26 00:00:00'},
                                                    {'item': '🍅', 'harvest': '2020-10-01 00:00:00'}])
                    | 'With timestamps per key' >> beam.Map(lambda crop: 
                                                    beam.window.TimestampedValue(crop['item'], 
                                                                                 to_unix_time(crop['harvest'])))
                    | 'Get latest element' >> beam.combiners.Latest.Globally()
                    | 'o/p 1' >> beam.Map(print))


logging.info("Latest elements for each key ...")
input_2 = (pipeline | 'create i/p 2' >> beam.Create([('spring',{'item': '🥬', 'harvest': '2020-02-24 00:00:00'}),
                                                    ('spring', {'item': '🍓', 'harvest': '2020-06-16 00:00:00'}),
                                                    ('summer', {'item': '🥕', 'harvest': '2020-07-17 00:00:00'}),
                                                    ('summer', {'item': '🍓', 'harvest': '2020-08-26 00:00:00'}),
                                                    ('summer', {'item': '🍆', 'harvest': '2020-09-04 00:00:00'}),
                                                    ('summer', {'item': '🥬', 'harvest': '2020-09-18 00:00:00'}),
                                                    ('summer', {'item': '🍅', 'harvest': '2020-09-22 00:00:00'}),
                                                    ('autumn', {'item': '🍅', 'harvest': '2020-10-01 00:00:00'}),
                                                    ('autumn', {'item': '🥬', 'harvest': '2020-10-20 00:00:00'}),
                                                    ('autumn', {'item': '🍆', 'harvest': '2020-10-26 00:00:00'}),
                                                    ('winter', {'item': '🥬', 'harvest': '2020-02-24 00:00:00'})])
                    | 'With timestamps' >> beam.Map(lambda pair: 
                                                    beam.window.TimestampedValue((pair[0], pair[1]['item']),
                                                                                 to_unix_time(pair[1]['harvest'])))
                    | 'Get latest elements per key' >> beam.combiners.Latest.PerKey()
                    | 'o/p 2' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()