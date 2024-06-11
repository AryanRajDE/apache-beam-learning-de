## `Map`

Map accepts a function that returns a single element for every input element in the PCollection.

Below I am discussing only complex fucntion of `beam.Map()`

---

### `Map with side inputs as singletons`

If the PCollection has a single value, such as the average from another computation, passing the PCollection as a singleton accesses that value.

--- 
### `Map with side inputs as iterators`

If the PCollection has multiple values, pass the PCollection as an iterator. This accesses elements lazily as they are needed, so it is possible to iterate over large PCollections that won’t fit into memory.


#### `Note:` You can pass the PCollection as a list with `beam.pvalue.AsList(pcollection)`, but this requires that all the elements fit into memory.

---
### `Map with side inputs as dictionaries`

If a PCollection is small enough to fit into memory, then that PCollection can be passed as a dictionary by using `beam.pvalue.AsDict(pcollection)`. Each element must be a `(key, value)` pair. 

`Note` that all the elements of the PCollection must fit into memory for this. 

If the PCollection won’t fit into memory, use `beam.pvalue.AsIter(pcollection)` instead.

---
### `MapTuple for key-value pairs`
If your PCollection consists of (key, value) pairs, you can use MapTuple to unpack them into different function arguments.

