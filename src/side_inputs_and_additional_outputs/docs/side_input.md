### `Side Input`

In addition to the main input `PCollection`, you can provide additional inputs to a `ParDo` transform in the form of `side inputs`. 

A **`Side Input`** is an additional input that your `DoFn` can access each time it processes an element in the input `PCollection`. When you specify a side input, you create a view of some other data that can be read from within the `ParDo` transform’s `DoFn` while processing each element.

**`Side inputs`** are useful if your ParDo needs to inject additional data when processing each element in the input PCollection, but the additional data needs to be determined at runtime (and not hard-coded). Such values might be determined by the input data, or depend on a different branch of your pipeline.

Side inputs are available as extra arguments in the `DoFn's` process method or `Map` / `FlatMap's` callable.

`Optional, positional, and keyword arguments` are all supported. `Deferred arguments` are unwrapped into their actual values. 

We can also pass side inputs to a `ParDo transform`, which will get passed to its `process` method.
The first two arguments for the process method would be **self** and **element**.

`For example`, using `pvalue.AsIteor(pcoll)` at pipeline construction time results in an iterable of the actual elements of pcoll being passed into each process invocation.

