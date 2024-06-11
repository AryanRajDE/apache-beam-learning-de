`1. ParDo with a simple DoFn`

The following example defines a simple DoFn class called SplitWords which stores the delimiter as an object field. The process method is called once per element, and it can yield zero or more output elements.

`2. ParDo with timestamp and window information`

In this, we add new parameters to the process method to bind parameter values at runtime.

`beam.DoFn.TimestampParam` binds the timestamp information as an apache_beam.utils.timestamp.Timestamp object.
`beam.DoFn.WindowParam` binds the window information as the appropriate apache_beam.transforms.window.*Window object.


`3. ParDo with DoFn methods`

A DoFn can be customized with a number of methods that can help create more complex behaviors. You can customize what a worker does when it starts and shuts down with setup and teardown. You can also customize what to do when a bundle of elements starts and finishes with start_bundle and finish_bundle.

`DoFn.setup():` Called whenever the DoFn instance is deserialized on the worker. This means it can be called more than once per worker because multiple instances of a given DoFn subclass may be created (e.g., due to parallelization, or due to garbage collection after a period of disuse). This is a good place to connect to database instances, open network connections or other resources.

`DoFn.start_bundle():` Called once per bundle of elements before calling process on the first element of the bundle. This is a good place to start keeping track of the bundle elements.

`DoFn.process(element, *args, **kwargs):` Called once per element, can yield zero or more elements. Additional *args or **kwargs can be passed through beam.ParDo(). [required]

`DoFn.finish_bundle():` Called once per bundle of elements after calling process after the last element of the bundle, can yield zero or more elements. This is a good place to do batch calls on a bundle of elements, such as running a database query.

For example, you can initialize a batch in start_bundle, add elements to the batch in process instead of yielding them, then running a batch query on those elements on finish_bundle, and yielding all the results.

`Note` that yielded elements from finish_bundle must be of the type apache_beam.utils.windowed_value.WindowedValue. You need to provide a timestamp as a unix timestamp, which you can get from the last processed element. You also need to provide a window, which you can get from the last processed element like in the example below.

`DoFn.teardown():` Called once (as a best effort) per DoFn instance when the DoFn instance is shutting down. This is a good place to close database instances, close network connections or other resources.

`Note` that teardown is called as a best effort and is not guaranteed. For example, if the worker crashes, teardown might not be called.