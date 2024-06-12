## `GroupBy`

GroupBy Takes a collection of elements and produces a collection grouped, by properties of those elements.
Unlike GroupByKey, the key is dynamically created from the elements themselves.

`GroupBy` can be performed via different ways :

`1.` by passing the expression via lambda

`2.` by passing multiple expressions via lambda

`3.` by passing an attribute from the input pcollection instead of the lambda expression

`4.` by passing the mix and match attribute and expression


## `Aggregation`

Grouping is often used in conjunction with aggregation, and the `aggregate_field` method of the `GroupBy` transform can be used to accomplish this easily. 

The `aggregate_field` method takes three parameters : 

`1.` the `field` (or `expression`) which to aggregate, 

`2.` the `CombineFn` (or associative `callable`) with which to aggregate by, 

`3.` and finally a field name `dest` in which to store the result. 

For example, suppose one wanted to compute the amount of each fruit to buy.