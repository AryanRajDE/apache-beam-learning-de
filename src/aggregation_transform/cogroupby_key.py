import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

def join_info(name_info):
  (name, info) = name_info
  return '%s : %s : %s' %(name, sorted(info['emails']), sorted(info['phones']))

# creating two pcollection named as email_list & phones_list
emails_list = [('amy', 'amy@example.com'),
               ('carl', 'carl@example.com'),
               ('julia', 'julia@example.com'),
               ('carl', 'carl@email.com')]

phones_list = [('amy', '111-222-3333'),
               ('james', '222-333-4444'),
               ('amy', '333-444-5555'),
               ('carl', '444-555-6666')]

emails = pipeline | 'Create Emails' >> beam.Create(emails_list)
phones = pipeline | 'Create Phones' >> beam.Create(phones_list)


# passing multiple pcollection as a dictionary and applying cogroupbykey()
results = ({'emails': emails, 'phones': phones} | beam.CoGroupByKey())

# passing cogroupbykey() result to sort out via the Map()
contact_lines = results | beam.Map(join_info) 

# printing the outputs
cogrp_result =  results | 'o/p 1' >> beam.Map(print)
pardo_result = contact_lines| 'o/p 2' >> beam.Map(print)


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()