import apache_beam as beam 
import logging

pipeline = beam.Pipeline() 

# Callable takes additional arguments.
def filter_using_length(word, lower_bound, upper_bound=float('inf')):
  if lower_bound <= len(word) <= upper_bound:
    yield word

# ParDo function 
class FilterUsingLength(beam.DoFn):
  def process(self, element, lower_bound, upper_bound=float('inf')):
    if lower_bound <= len(element) <= upper_bound:
      yield element


# creating a word input
words = pipeline | 'create word' >> beam.Create(["SamuelJohn"])    #10-letters
# created_word = words | beam.Map(print)

# Construct a deferred side input.
avg_word_len = (words | 'word length' >> beam.Map(len) 
                      | 'Combine Mean' >> beam.CombineGlobally(beam.combiners.MeanCombineFn()))
                    #   | 'o/p 1' >> beam.Map(print))

# Call with explicit side inputs.
small_words = (words | 'small' >> beam.FlatMap(filter_using_length, 
                                              lower_bound=0, 
                                              upper_bound=13) 
                     | 'o/p 2' >> beam.Map(print))

# A single deferred side input.
larger_than_average = (words | 'large' >> beam.FlatMap(filter_using_length, 
                                                       lower_bound=beam.pvalue.AsSingleton(avg_word_len))
                             | 'o/p 3' >> beam.Map(print))

# Mix and match.
small_but_nontrivial = words | 'mix and match' >> beam.FlatMap(filter_using_length,
                                                               lower_bound=0,
                                                               upper_bound=beam.pvalue.AsSingleton(avg_word_len)
                             | 'o/p 4' >> beam.Map(print))


# We can also pass side inputs to a ParDo transform, which will get passed to its process method.
# The first two arguments for the process method would be self and element.
small_words_with_pardo = (words | 'with par_do' >> beam.ParDo(FilterUsingLength(),
                                                              lower_bound=0,
                                                              upper_bound=beam.pvalue.AsSingleton(avg_word_len)) 
                                | 'o/p 5' >> beam.Map(print))


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()