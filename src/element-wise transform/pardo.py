import logging
import apache_beam as beam

class LowerCaseConversion(beam.DoFn):
    def process(self, element):
        return [element.lower()]
    

class SplitWords(beam.DoFn):
    def __init__(self, delimiter=','):
      self.delimiter = delimiter

    def process(self, text):
      for word in text.split(self.delimiter):
        yield word
    

class AnalyzeElement(beam.DoFn):
    def process(self, elem, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
       """
       we add new parameters to the process method to bind parameter values at runtime.
       beam.DoFn.TimestampParam : binds the timestamp information as an apache_beam.utils.timestamp.Timestamp object.
       beam.DoFn.WindowParam : binds the window information as the appropriate apache_beam.transforms.window.*Window object.
       """

       yield '\n'.join([
          '# timestamp',
          'type(timestamp) -> ' + repr(type(timestamp)),
          'timestamp.micros -> ' + repr(timestamp.micros),
          'timestamp.to_rfc3339() -> ' + repr(timestamp.to_rfc3339()),
          'timestamp.to_utc_datetime() -> ' + repr(timestamp.to_utc_datetime()),
          '',
          '# window',
          'type(window) -> ' + repr(type(window)),
          'window.start -> {} ({})'.format(
              window.start, window.start.to_utc_datetime()),
          'window.end -> {} ({})'.format(
              window.end, window.end.to_utc_datetime()),
          'window.max_timestamp() -> {} ({})'.format(
              window.max_timestamp(), window.max_timestamp().to_utc_datetime()),
      ])
       

with beam.Pipeline() as pipeline:
    
    print("ParDo with basic DoFn ...")
    names = pipeline \
        | 'Names' >> beam.Create(['John', 'Mike', 'Sam']) \
        | 'Lower' >> beam.ParDo(LowerCaseConversion()) \
        | 'Names O/P' >> beam.Map(print)
    
    plants = (pipeline
                | 'Gardening plants' >> beam.Create(['Strawberry,Carrot,Eggplant',
                                                   'Tomato,Potato'])
                | 'Split words' >> beam.ParDo(SplitWords(','))
                | 'Plant O/P' >> beam.Map(print))
    

    print("ParDo with timestamp and window information ...")
    dofn_params = (pipeline
                   | 'Create a single test element' >> beam.Create([':)'])
                   | 'Add timestamp' >> beam.Map(lambda elem: beam.window.TimestampedValue(elem, 1584675660))
                   | 'Fixed 30sec windows' >> beam.WindowInto(beam.window.FixedWindows(30))
                   | 'Analyze element' >> beam.ParDo(AnalyzeElement())
                   | 'Timestamp O/P' >> beam.Map(print))
    

    print("ParDo with complex DoFn methods ...")

    


# logging.getLogger().setLevel(logging.INFO)
# pipeline.run().wait_until_finish()
             