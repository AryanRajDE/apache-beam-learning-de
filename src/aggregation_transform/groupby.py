import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

logging.info("Creating beam row input ...")
GROCERY_LIST = [beam.Row(recipe='pie', fruit='raspberry', quantity=1, unit_price=3.50),
                beam.Row(recipe='pie', fruit='blackberry', quantity=1, unit_price=4.00),
                beam.Row(recipe='pie', fruit='blueberry', quantity=1, unit_price=2.00),
                beam.Row(recipe='muffin', fruit='blueberry', quantity=2, unit_price=2.00),
                beam.Row(recipe='muffin', fruit='banana', quantity=3, unit_price=1.00)]


logging.info("GroupBy to group all fruits by the first letter of their name. ...")
input_1 = (pipeline | 'create i/p 1' >> beam.Create( ['strawberry', 'raspberry', 'blueberry', 'blackberry', 'banana'])
           | 'GroupBy Elements' >> beam.GroupBy(lambda word: word[0])
           | 'o/p 1' >> beam.Map(print))


logging.info("GroupBy to group by a composite key consisting of multiple properties if desired. ...")
input_2 = (pipeline | 'create i/p 2' >> beam.Create(['strawberry', 'raspberry', 'blueberry', 'blackberry', 'banana'])
           | 'GroupBy Elements by two expressions' >> beam.GroupBy(letter=lambda word: word[0],
                                                                   is_berry=lambda word: 'berry' in word)
           | 'o/p 2' >> beam.Map(print))


logging.info("GroupBy an attribute, a string may be passed to GroupBy in the place of a callable expression. ...")
input_3 = (pipeline | 'create i/p 3' >> beam.Create(GROCERY_LIST)
           | 'GroupBy Elements by attribute' >> beam.GroupBy('recipe')
           | 'o/p 3' >> beam.Map(print))


logging.info("GroupBy using mix and match attributes and expressions. ...")
input_4 = (pipeline | 'create i/p 4' >> beam.Create(GROCERY_LIST)
           | 'GroupBy Elements by attribute & expression' >> beam.GroupBy('recipe', 
                                                                          is_berry=lambda x: 'berry' in x.fruit)
           | 'o/p 4' >> beam.Map(print))


logging.info("Aggregation ...")
logging.info("GroupBy simple aggregate. ...")
input_5 = (pipeline | 'create i/p 5' >> beam.Create(GROCERY_LIST)
           | 'GroupBy simple aggregate' >> beam.GroupBy('fruit').aggregate_field(field='quantity',
                                                                                 combine_fn=sum,
                                                                                 dest='total_quantity')
           | 'o/p 5' >> beam.Map(print))


logging.info("GroupBy multiple aggregate. ...")
input_6 = (pipeline | 'create i/p 6' >> beam.Create(GROCERY_LIST)
           | 'GroupBy multiple aggregate' >> beam.GroupBy('recipe')
                        .aggregate_field(field='quantity', combine_fn=sum, dest='total_quantity')
                        .aggregate_field(field=lambda x: x.unit_price * x.quantity,
                                         combine_fn=sum,
                                         dest='price')
           | 'o/p 6' >> beam.Map(print))


logging.info("GroupBy multiple aggregate by same field. ...")
input_7 = (pipeline | 'create i/p 7' >> beam.Create(GROCERY_LIST)
           | 'GroupBy aggregate by same field' >> beam.GroupBy()
                        .aggregate_field(field='unit_price', combine_fn=min, dest='min_price')
                        .aggregate_field(field='unit_price', combine_fn=beam.combiners.MeanCombineFn(), dest='mean_price')
                        .aggregate_field(field='unit_price', combine_fn=max, dest='max_price')
           | 'o/p 7' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()