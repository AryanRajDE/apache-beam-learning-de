## `GroupByKey`

### `Input to GroupByKey`

The input to `GroupByKey` is a combination of `key/value pairs` that describe a multimap, i.e., multiple pairs with the same key but different values. For such cases, you use GroupByKey to collect all the values connected with each unique key.

Let’s take an example where we have words (keys) from a text file and the line numbers (values) on which they appear. Our goal is to combine all the line numbers for a particular word.

I, 3
We, 6
You, 7
They, 9
Edpresso, 1
Educative, 2
You, 5
They, 4
Edpresso, 3
Educative, 8

### `Output of GroupByKey`
As discussed above, our goal is to get all the line numbers for a particular word.
Applying GroupByKey to this input, we get the output as:

I, [3]
We, [6]
You, [7, 5]
They, [9, 4]
Edpresso, [1,3]
Educative, [2,8]

The `GroupByKey` transform is for **bounded** data. To apply `GroupByKey` to **unbounded** data, you need to use windowing, otherwise Beam generates `IllegalStateException` while building the pipeline.