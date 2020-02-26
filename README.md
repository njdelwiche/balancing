# Balancing Groups
 
This script creates balanced sub-groups from a larger roster. After loading in a csv roster, the user can specify the group sizes and criteria along which they are balancing.

The program first examines the overall distribution of values across the balance criteria and sets a ceiling for the number each group can contain (e.g. 15 males). 

It then balances the groups by semi-randomly swapping items. It ensures not to backtrack through swaps by:
 
* Creating the first sub-group by extracting a sample from the larger roster
* Checking the balance of that first sub-group
* Swapping items in the first sub-group with only items from the larger roster
* Once the first group is finished, it breaks another sub-group from the larger roster 
* It then swaps items in the second-group with only the larger (yet now slightly diminished) roster, leaving the first group untouched
* It continues until all groups are balanced 
