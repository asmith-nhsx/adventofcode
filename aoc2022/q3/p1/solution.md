
# Helpers

    ## ── Attaching packages ─────────────────────────────────────── tidyverse 1.3.2 ──
    ## ✔ ggplot2 3.4.0      ✔ purrr   0.3.5 
    ## ✔ tibble  3.1.8      ✔ dplyr   1.0.10
    ## ✔ tidyr   1.2.1      ✔ stringr 1.5.0 
    ## ✔ readr   2.1.3      ✔ forcats 0.5.2 
    ## ── Conflicts ────────────────────────────────────────── tidyverse_conflicts() ──
    ## ✖ dplyr::filter() masks stats::filter()
    ## ✖ dplyr::lag()    masks stats::lag()

# Day 3: Rucksack Reorganization

One Elf has the important job of loading all of the rucksacks with
supplies for the jungle journey. Unfortunately, that Elf didn’t quite
follow the packing instructions, and so a few items now need to be
rearranged.

Each rucksack has two large compartments. All items of a given type are
meant to go into exactly one of the two compartments. The Elf that did
the packing failed to follow this rule for exactly one item type per
rucksack.

The Elves have made a list of all of the items currently in each
rucksack (your puzzle input), but they need your help finding the
errors. Every item type is identified by a single lowercase or uppercase
letter (that is, a and A refer to different types of items).

The list of items for each rucksack is given as characters all on a
single line. A given rucksack always has the same number of items in
each of its two compartments, so the first half of the characters
represent items in the first compartment, while the second half of the
characters represent items in the second compartment.

For example, suppose you have the following list of contents from six
rucksacks:

    vJrwpWtwJgWrhcsFMMfFFhFp
    jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    PmmdzqPrVvPwwTWBwg
    wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ttgJtRGJQctTZtZT
    CrZsJsPPZsGzwwsLwLmpwMDw

The first rucksack contains the items `vJrwpWtwJgWrhcsFMMfFFhFp`, which
means its first compartment contains the items `vJrwpWtwJgWr`, while the
second compartment contains the items `hcsFMMfFFhFp`. The only item type
that appears in both compartments is lowercase p. The second rucksack’s
compartments contain `jqHRNqRjqzjGDLGL` and `rsFMfFZSrLrFZsSL`. The only
item type that appears in both compartments is uppercase L. The third
rucksack’s compartments contain `PmmdzqPrV` and `vPwwTWBwg`; the only
common item type is uppercase P. The fourth rucksack’s compartments only
share item type v. The fifth rucksack’s compartments only share item
type t. The sixth rucksack’s compartments only share item type s. To
help prioritize item rearrangement, every item type can be converted to
a priority:

Lowercase item types a through z have priorities 1 through 26. Uppercase
item types A through Z have priorities 27 through 52. In the above
example, the priority of the item type that appears in both compartments
of each rucksack is 16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19 (s);
the sum of these is `157`.

Find the item type that appears in both compartments of each rucksack.
What is the sum of the priorities of those item types?

# Solution

``` r
prioritize <- function(it) {
  code <- as.integer(charToRaw(it))
  if (str_detect(it, "[[:upper:]]")) {
    return(code - 38)
  } else {
    return(code - 96)
  }
}

solve <- function(x) {
  x$len <- nchar(x$V1)
  x$c1 <- strsplit(substr(x$V1, 0, x$len/2),"")
  x$c2 <- strsplit(substr(x$V1, x$len/2+1, x$len),"")
  x$duplicate <- apply(x[c("c1","c2")], 1, function(d) { toString(intersect(unlist(d[1]), unlist(d[2]))) })
  x$priority <- apply(x["duplicate"], 1, prioritize)
  return(sum(x$priority))
}
```

# Test

Start by loading test data then apply solve.

``` r
harness(157, solve)
```

    ## [1] "Passed"

    ## [1] 157

# Answer

Your puzzle answer was `7766`.

``` r
harness(7766, solve, FALSE)
```

    ## [1] "Passed"

    ## [1] 7766
