### `Additional Outputs`

While `ParDo` always produces a main output `PCollection` (as the return value from apply), you can also have your `ParDo` produce any number of `additional output PCollections`. 

If you choose to have multiple outputs, your `ParDo` returns all of the `output PCollections` (including the main output) bundled together.

To emit elements to multiple `output PCollections`, invoke **`with_outputs()`** on the `ParDo`, and specify the
expected tags for the outputs. 

`with_outputs()` returns a `DoOutputsTuple` object. 

Tags specified in `with_outputs` are attributes on the returned `DoOutputsTuple` object. The tags give access to the corresponding `output PCollections`.

Inside your `ParDo's DoFn`, you can emit an element to a specific output by wrapping the value and the output tag (str) using the `beam.pvalue.OutputValue` wrapper class.

