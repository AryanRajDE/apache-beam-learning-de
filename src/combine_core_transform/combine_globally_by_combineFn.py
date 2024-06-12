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


def combineglobally_combinefn(test=None):
  # [START combineglobally_combinefn]
  import apache_beam as beam

  class PercentagesFn(beam.CombineFn):
    def create_accumulator(self):
      return {}

    def add_input(self, accumulator, input):
      # accumulator == {}
      # input == '🥕'
      if input not in accumulator:
        accumulator[input] = 0  # {'🥕': 0}
      accumulator[input] += 1  # {'🥕': 1}
      return accumulator

    def merge_accumulators(self, accumulators):
      # accumulators == [
      #     {'🥕': 1, '🍅': 2},
      #     {'🥕': 1, '🍅': 1, '🍆': 1},
      #     {'🥕': 1, '🍅': 3},
      # ]
      merged = {}
      for accum in accumulators:
        for item, count in accum.items():
          if item not in merged:
            merged[item] = 0
          merged[item] += count
      # merged == {'🥕': 3, '🍅': 6, '🍆': 1}
      return merged

    def extract_output(self, accumulator):
      # accumulator == {'🥕': 3, '🍅': 6, '🍆': 1}
      total = sum(accumulator.values())  # 10
      percentages = {item: count / total for item, count in accumulator.items()}
      # percentages == {'🥕': 0.3, '🍅': 0.6, '🍆': 0.1}
      return percentages

  with beam.Pipeline() as pipeline:
    percentages = (
        pipeline
        | 'Create produce' >> beam.Create(
            ['🥕', '🍅', '🍅', '🥕', '🍆', '🍅', '🍅', '🍅', '🥕', '🍅'])
        | 'Get percentages' >> beam.CombineGlobally(PercentagesFn())
        | beam.Map(print))
    # [END combineglobally_combinefn]
    if test:
      test(percentages)


if __name__ == '__main__':
  combineglobally_combinefn()
