"""Combining with a CombineFn
The more general way to combine elements, and the most flexible, is with a class that inherits from CombineFn.

1. CombineFn.create_accumulator(): This creates an empty accumulator. 
For example, an empty accumulator for a sum would be 0, while an empty accumulator for a product (multiplication) would be 1.

2. CombineFn.add_input(): Called once per element. 
Takes an accumulator and an input element, combines them and returns the updated accumulator.

3. CombineFn.merge_accumulators(): Multiple accumulators could be processed in parallel, 
so this function helps merging them into a single accumulator.

4. CombineFn.extract_output(): It allows to do additional calculations before extracting a result.
"""

import apache_beam as beam

def combineperkey_combinefn(test=None):
  # [START combineperkey_combinefn]
  import apache_beam as beam

  class AverageFn(beam.CombineFn):
    def create_accumulator(self):
      sum = 0.0
      count = 0
      accumulator = sum, count
      return accumulator

    def add_input(self, accumulator, input):
      sum, count = accumulator
      return sum + input, count + 1

    def merge_accumulators(self, accumulators):
      # accumulators = [(sum1, count1), (sum2, count2), (sum3, count3), ...]
      sums, counts = zip(*accumulators)
      # sums = [sum1, sum2, sum3, ...]
      # counts = [count1, count2, count3, ...]
      return sum(sums), sum(counts)

    def extract_output(self, accumulator):
      sum, count = accumulator
      if count == 0:
        return float('NaN')
      return sum / count

  with beam.Pipeline() as pipeline:
    average = (
        pipeline
        | 'Create plant counts' >> beam.Create([
            ('🥕', 3),
            ('🥕', 2),
            ('🍆', 1),
            ('🍅', 4),
            ('🍅', 5),
            ('🍅', 3),
        ])
        | 'Average' >> beam.CombinePerKey(AverageFn())
        | beam.Map(print))
    # [END combineperkey_combinefn]
    if test:
      test(average)


if __name__ == '__main__':
  combineperkey_combinefn()
