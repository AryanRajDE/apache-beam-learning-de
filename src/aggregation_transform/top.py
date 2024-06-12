import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

element_pcoll =  (pipeline | 'create element pcoll' >> beam.Create([1, 2, 3, 6, 44, 98]))
keyed_pcoll = (pipeline | 'create keyed pcoll' >> beam.Create([('spring', 2),
                                                                ('spring', 6),
                                                                ('summer', 0),
                                                                ('fall', 1),
                                                                ('spring', 2),
                                                                ('winter', 3),
                                                                ('spring', 2),
                                                                ('summer', 4),
                                                                ('fall', 1),
                                                                ('summer', 0)]))


logging.info(" Largest elements from a PCollection...")
input_1 = (element_pcoll | 'Largest N Values' >> beam.combiners.Top.Largest(n=2)
                         | 'o/p 1' >> beam.Map(print))

logging.info(" Largest elements for each key...")
input_2 = (keyed_pcoll | 'Largest N Values per key' >> beam.combiners.Top.LargestPerKey(n=2)
                         | 'o/p 2' >> beam.Map(print))

logging.info(" Smallest elements from a PCollection...")
input_3 = (element_pcoll | 'Smallest N Values' >> beam.combiners.Top.Smallest(n=2)
                         | 'o/p 3' >> beam.Map(print))

logging.info(" Smallest elements for each key...")
input_4 = (keyed_pcoll | 'Smallest N Values per key' >> beam.combiners.Top.SmallestPerKey(n=1)
                         | 'o/p 4' >> beam.Map(print))


logging.info(""" Custom elements from a PCollection.
             We use Top.Of() to get elements with customized rules from the entire PCollection.
             You can change how the elements are compared with key. 
             By default you get the largest elements, but you can get the smallest by setting reverse=True.""")

shortest_elements = (pipeline | 'Create i/p 5' >> beam.Create(['🍓 Strawberry',
                                                                '🥕 Carrot',
                                                                '🍏 Green apple',
                                                                '🍆 Eggplant',
                                                                '🌽 Corn'])
                              | 'Shortest names' >> beam.combiners.Top.Of(n=2,   # number of elements
                                                                         key=len,  # optional, defaults to the element itself
                                                                         reverse=True)  # optional, defaults to False (largest/descending)
                              | 'o/p 5' >> beam.Map(print))


logging.info(""" Custom elements for each key.
             We use Top.PerKey() to get elements with customized rules for each unique key in a PCollection of key-values.
             You can change how the elements are compared with key. 
             By default you get the largest elements, but you can get the smallest by setting reverse=True. """)

shortest_elements_per_key = (pipeline | 'Create i/p 6' >> beam.Create([('spring', '🥕 Carrot'),
                                                                    ('spring', '🍓 Strawberry'),
                                                                    ('summer', '🥕 Carrot'),
                                                                    ('summer', '🌽 Corn'),
                                                                    ('summer', '🍏 Green apple'),
                                                                    ('fall', '🥕 Carrot'),
                                                                    ('fall', '🍏 Green apple'),
                                                                    ('winter', '🍆 Eggplant')])
            | 'Shortest names per key' >> beam.combiners.Top.PerKey(n=2,   # number of elements
                                                        key=len,  # optional, defaults to the element itself
                                                        reverse=False)  # optional, defaults to False (largest/descending)
            | 'o/p 6' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()