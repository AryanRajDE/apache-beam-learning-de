import apache_beam as beam 

pipeline = beam.Pipeline()

print("Creating List data type in beam ...")
list_data = pipeline | 'create list' >> beam.Create(['Sam', 'John', 'Albert']) | 'list o/p' >> beam.Map(print)


print("Creating Tuple data type in beam ...")
tuple_data = pipeline | 'create tuple' >> beam.Create(('Samuel', 'Jacob', 'Adam')) | 'tuple o/p' >> beam.Map(print)


print("Creating Set data type in beam ...")
# duplicate element will get removed from set 
set_data = pipeline | 'create set' >> beam.Create({'Sam', 'John', 'Albert', 'John', 'Sam'}) | 'set o/p' >> beam.Map(print)


print("Creating dict data type in beam ...")
dict_data_1 = pipeline | 'create dict 1' >> beam.Create({'Sam':1, 'John':2, 'Adam':3}) | 'dict o/p 1' >> beam.Map(print)

dict_data_2 = pipeline | 'create dict 2' >> beam.Create(('Sam', 1), 
                                                        ('John', 2), 
                                                        ('Adam', 3)) | 'dict o/p 2' >> beam.Map(print)

result = pipeline.run()
result.wait_until_finish()