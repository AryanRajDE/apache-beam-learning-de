import apache_beam as beam 
import logging

pipeline = beam.Pipeline()

def even_odd(x):
  yield beam.pvalue.TaggedOutput('odd' if x % 2 else 'even', x)
  if x % 10 == 0:
    yield x

# ParDo function 
class ProcessWords(beam.DoFn):
  def process(self, element, cutoff_length, marker):
    if len(element) <= cutoff_length:
      # Emit this short word to the main output.
      yield element
    else:
      # Emit this word's long length to the 'above_cutoff_lengths' output.
      yield beam.pvalue.TaggedOutput('above_cutoff_lengths', len(element))
    if element.startswith(marker):
      # Emit this word to a different output with the 'marked strings' tag.
      yield beam.pvalue.TaggedOutput('marked strings', element)


# creating a word input
words = pipeline | 'create word' >> beam.Create(["SamuelJohn"])    # or xSamuelJohn
# created_word = words | beam.Map(print)

results = (words| beam.ParDo(ProcessWords(), 
                             cutoff_length=3, 
                             marker='x').with_outputs('above_cutoff_lengths',
                                                      'marked strings',
                                                      main='below_cutoff_strings'))

# getting the multiple additional pcollections
below = results.below_cutoff_strings | 'o/p 1' >> beam.Map(print)
above = results.above_cutoff_lengths | 'o/p 2' >> beam.Map(print) 
marked = results['marked strings']  | 'o/p 3' >> beam.Map(print)    # indexing works as well


# The result is also iterable, ordered in the same order that the tags were passed to with_outputs(),
# the main tag (if specified) first.
below, above, marked = (words| 'tag along' >> beam.ParDo(ProcessWords(),
                                                         cutoff_length=2,
                                                         marker='x').with_outputs('above_cutoff_lengths',
                                                                                  'marked strings',
                                                                                  main='below_cutoff_strings'))
below | 'o/p 4' >> beam.Map(print)
above | 'o/p 5' >> beam.Map(print)
marked | 'o/p 6' >> beam.Map(print)


# Producing multiple outputs is also available in Map and FlatMap.
# Here is an example that uses FlatMap and shows that the tags do not need to be specified ahead of time.

numbers = pipeline | 'create number' >> beam.Create([100])   
# created_number = numbers | beam.Map(print)

results = numbers | beam.FlatMap(even_odd).with_outputs()

evens = results.even | 'o/p 6' >> beam.Map(print)
odds = results.odd | 'o/p 7' >> beam.Map(print)
tens = results[None]  | 'o/p 8' >> beam.Map(print)  # the undeclared main output


# running the beam pipeline
result = pipeline.run()
result.wait_until_finish()