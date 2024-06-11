import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

logging.info("Reify transformation ...")
"""Transforms for converting between explicit and implicit form of various Beam values."""

input_1 = (pipeline | 'create i/p 1' >> beam.Create([('1', 'Strawberry'),
                                                    ('2', 'Carrot'),
                                                    ('3', 'Eggplant'),
                                                    ('4', 'Tomato'),
                                                    ('5', 'Potato')]))

single_input = (pipeline | 'Create a single test element' >> beam.Create([':)']))

# reify_1 = (single_input | 'Add timestamp' >> beam.Map(lambda elem: beam.window.TimestampedValue(elem, 1584675660))
#                    | 'Fixed 30sec windows' >> beam.WindowInto(beam.window.FixedWindows(30))
#                    | 'reify via timestamp' >> beam.Reify.Timestamp().add_timestamp_info(elem, timestamp=timestamp.to_utc_datetime()) 
#                    | beam.LogElements())

reify_2 = (single_input | beam.Reify.Window.add_window_info(single_input, 
                                                            timestamp=beam.window.TimestampedValue(single_input, 1584675660), 
                                                            window=beam.window.FixedWindows(30))
                        | beam.LogElements())

# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()