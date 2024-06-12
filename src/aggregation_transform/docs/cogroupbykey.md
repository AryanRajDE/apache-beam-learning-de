### `CoGroupByKey`

`CoGroupByKey` performs a relational join of two or more key/value PCollections that have the same key type.

`CoGroupByKey` aggregates all input elements by their key and allows downstream processing to consume all values associated with the key. 

While `GroupByKey` performs this operation over a single input collection and thus a single type of input values, `CoGroupByKey` operates over multiple input collections. As a result, the result for each key is a tuple of the values associated with that key in each input collection.

Consider using `CoGroupByKey` if you have multiple data sets that provide information about related things. 

`For example` :

let’s say you have two different files with user data: one file has names and email addresses; the other file has names and phone numbers. You can join those two data sets, using the user name as a common key and the other data as the associated values. After the join, you have one data set that contains all of the information (email addresses and phone numbers) associated with each name.
One can also consider using SqlTransform to perform a join.

If you are using unbounded PCollections, you must use either non-global windowing or an aggregation trigger in order to perform a CoGroupByKey. 

In the `Beam SDK for Python`, **CoGroupByKey** accepts a dictionary of keyed PCollections as input. As output, CoGroupByKey creates a single output PCollection that contains one key/value tuple for each key in the input PCollections. Each key’s value is a dictionary that maps each tag to an iterable of the values under they key in the corresponding PCollection.