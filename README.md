# Balancing Groups
 
This program helps create balanced sub-groups from a larger roster. After loading in a "roster.csv" file, the user can edit the group sizes and criteria along which they are balancing.

The program first examines the overall distribution of values across the balance criteria and sets a ceiling for the number each group can contain (e.g. 15 males). 

It then balances the groups by semi-randomly swapping items. It ensures not to backtrack through swaps by:
 
* Creating the first sub-group by extracting a sample from the larger roster
* Checking the balance of that first sub-group
* Swapping items in the first sub-group with only items from the larger roster
* Once the first group is finished, it breaks another sub-group from the larger roster 
* It then swaps items in the second-group with only the larger (yet now slightly diminished) roster, leaving the first group untouched
* It continues until all groups are balanced 

It then ensures that the swaps have not changed the overall, groups-total distribution of values. Finally, it outputs a csv file with a new column that indicates the balanced group pairings.
