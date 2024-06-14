# Test Your Pipeline

Testing your pipeline is a particularly important step in developing an effective data processing solution. The indirect nature of the Beam model, in which your user code constructs a pipeline graph to be executed remotely, can make debugging failed runs a non-trivial task. Often it is faster and simpler to perform local unit testing on your pipeline code than to debug a pipeline’s remote execution.

Before running your pipeline on the runner of your choice, unit testing your pipeline code locally is often the best way to identify and fix bugs in your pipeline code. Unit testing your pipeline locally also allows you to use your familiar/favorite local debugging tools.

You can use [DirectRunner](https://beam.apache.org/documentation/runners/direct), a local runner helpful for testing and local development.

After you test your pipeline using the `DirectRunner`, you can use the runner of your choice to test on a small scale. For example, use the Flink runner with a local or remote Flink cluster.

The Beam SDKs provide a number of ways to unit test your pipeline code, from the lowest to the highest levels. From the lowest to the highest level, these are:

* You can test the individual functions used in your pipeline.
* You can test an entire [Transform](https://beam.apache.org/documentation/programming-guide/#composite-transforms) as a unit.
* You can perform an end-to-end test for an entire pipeline.

To support unit testing, the Beam SDK for Java provides a number of test classes in the [testing package](https://github.com/apache/beam/tree/master/sdks/java/core/src/test/java/org/apache/beam/sdk). You can use these tests as references and guides.

## Testing Transforms

To test a transform you’ve created, you can use the following pattern:

* Create a `TestPipeline`.
* Create some static, known test input data.
* Use the `Create` transform to create a `PCollection` of your input data.
* `Apply` your transform to the input `PCollection` and save the resulting output `PCollection`.
* Use `PAssert` and its subclasses to verify that the output `PCollection` contains the elements that you expect.

### TestPipeline

[TestPipeline](https://github.com/apache/beam/blob/master/sdks/python/apache_beam/testing/test_pipeline.py) is a class included in the Beam Python SDK specifically for testing transforms.

For tests, use `TestPipeline` in place of `Pipeline` when you create the pipeline object. Unlike `Pipeline.create`, `TestPipeline.create` handles setting `PipelineOptions` internally.

You create a `TestPipeline` as follows:

```python
with TestPipeline as p:
    ...
```

> **Note:** Read about testing unbounded pipelines in Beam in [this blog post](https://beam.apache.org/blog/2016/10/20/test-stream.html).

### Using the Create Transform

You can use the `Create` transform to create a `PCollection` out of a standard in-memory collection class, such as Java or Python `List`. See [Creating a PCollection](https://beam.apache.org/documentation/programming-guide/#creating-a-pcollection) for more information.

### PAssert

[PAssert](https://beam.apache.org/releases/javadoc/2.56.0/index.html?org/apache/beam/sdk/testing/PAssert.html) is a class included in the Beam Java SDK that is an assertion on the contents of a `PCollection`. You can use `PAssert`to verify that a `PCollection` contains a specific set of expected elements.

For a given `PCollection`, you can use `PAssert` to verify the contents as follows:

```python
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to

output = ...

# Check whether a PCollection contains some elements in any order.
assert_that(output, equal_to(["elem1", "elem3", "elem2"]))
```

For more information on how these classes work, see the [org.apache.beam.sdk.testing](https://beam.apache.org/releases/javadoc/2.56.0/index.html?org/apache/beam/sdk/testing/package-summary.html) package documentation.

### An Example Test for a Composite Transform

The following code shows a complete test for a composite transform. The test applies the `Count` transform to an input `PCollection` of `String` elements. The test uses the `Create` transform to create the input `PCollection` from a `List<String>`.

```python
import unittest
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to

class CountTest(unittest.TestCase):

  def test_count(self):
    # Our static input data, which will make up the initial PCollection.
    WORDS = [
      "hi", "there", "hi", "hi", "sue", "bob",
      "hi", "sue", "", "", "ZOW", "bob", ""
    ]
    # Create a test pipeline.
    with TestPipeline() as p:

      # Create an input PCollection.
      input = p | beam.Create(WORDS)

      # Apply the Count transform under test.
      output = input | beam.combiners.Count.PerElement()

      # Assert on the results.
      assert_that(output, equal_to([("hi", 4),
				    ("there", 1),
            			    ("sue", 2),
            			    ("bob", 2),
           			    ("", 3),
           			    ("ZOW", 1)]))

      # The pipeline will run and verify the results.
```

## Testing a Pipeline End-to-End

You can use the test classes in the Beam SDKs (such as `TestPipeline` and `PAssert` in the Beam SDK for Java) to test an entire pipeline end-to-end. Typically, to test an entire pipeline, you do the following:

* For every source of input data to your pipeline, create some known static test input data.
* Create some static test output data that matches what you expect in your pipeline’s final output `PCollection`(s).
* Create a `TestPipeline` in place of the standard `Pipeline.create`.
* In place of your pipeline’s `Read` transform(s), use the `Create` transform to create one or more `PCollection`s from your static input data.
* Apply your pipeline’s transforms.
* In place of your pipeline’s `Write` transform(s), use `PAssert` to verify that the contents of the final `PCollection`s your pipeline produces match the expected values in your static output data.

### Testing the WordCount Pipeline

The following example code shows how one might test the [WordCount example pipeline](https://beam.apache.org/get-started/wordcount-example/). `WordCount` usually reads lines from a text file for input data; instead, the test creates a `List<String>` containing some text lines and uses a `Create` transform to create an initial `PCollection`.

`WordCount`’s final transform (from the composite transform `CountWords`) produces a `PCollection<String>` of formatted word counts suitable for printing. Rather than write that `PCollection` to an output text file, our test pipeline uses `PAssert` to verify that the elements of the `PCollection` match those of a static `String` array containing our expected output data.

```python
import unittest
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to

class CountWords(beam.PTransform):
    # CountWords transform omitted for conciseness.
    # Full transform can be found here - https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/wordcount_debugging.py

class WordCountTest(unittest.TestCase):

  # Our input data, which will make up the initial PCollection.
  WORDS = [
      "hi", "there", "hi", "hi", "sue", "bob",
      "hi", "sue", "", "", "ZOW", "bob", ""
  ]

  # Our output data, which is the expected data that the final PCollection must match.
  EXPECTED_COUNTS = ["hi: 5", "there: 1", "sue: 2", "bob: 2"]

  # Example test that tests the pipeline's transforms.

  def test_count_words(self):
    with TestPipeline() as p:

      # Create a PCollection from the WORDS static input data.
      input = p | beam.Create(WORDS)

      # Run ALL the pipeline's transforms (in this case, the CountWords composite transform).
      output = input | CountWords()

      # Assert that the output PCollection matches the EXPECTED_COUNTS data.
      assert_that(output, equal_to(EXPECTED_COUNTS), label='CheckOutput')

    # The pipeline will run and verify the results.
```
