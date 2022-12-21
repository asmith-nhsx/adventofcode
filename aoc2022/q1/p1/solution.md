
# Helpers

    ## ── Attaching packages ─────────────────────────────────────── tidyverse 1.3.2 ──
    ## ✔ ggplot2 3.4.0      ✔ purrr   0.3.5 
    ## ✔ tibble  3.1.8      ✔ dplyr   1.0.10
    ## ✔ tidyr   1.2.1      ✔ stringr 1.5.0 
    ## ✔ readr   2.1.3      ✔ forcats 0.5.2 
    ## ── Conflicts ────────────────────────────────────────── tidyverse_conflicts() ──
    ## ✖ dplyr::filter() masks stats::filter()
    ## ✖ dplyr::lag()    masks stats::lag()

# Day 1: Calorie Counting

Santa’s reindeer typically eat regular reindeer food, but they need a
lot of magical energy to deliver presents on Christmas. For that, their
favorite snack is a special type of star fruit that only grows deep in
the jungle. The Elves have brought you on their annual expedition to the
grove where the fruit grows.

To supply enough magical energy, the expedition needs to retrieve a
minimum of fifty stars by December 25th. Although the Elves assure you
that the grove has plenty of fruit, you decide to grab any fruit you see
along the way, just in case.

Collect stars by solving puzzles. Two puzzles will be made available on
each day in the Advent calendar; the second puzzle is unlocked when you
complete the first. Each puzzle grants one star. Good luck!

The jungle must be too overgrown and difficult to navigate in vehicles
or access from the air; the Elves’ expedition traditionally goes on
foot. As your boats approach land, the Elves begin taking inventory of
their supplies. One important consideration is food - in particular, the
number of Calories each Elf is carrying (your puzzle input).

The Elves take turns writing down the number of Calories contained by
the various meals, snacks, rations, etc. that they’ve brought with them,
one item per line. Each Elf separates their own inventory from the
previous Elf’s inventory (if any) by a blank line.

For example, suppose the Elves finish writing their items’ Calories and
end up with the following list:

    1000
    2000
    3000

    4000

    5000
    6000

    7000
    8000
    9000

    10000

This list represents the Calories of the food carried by five Elves:

The first Elf is carrying food with 1000, 2000, and 3000 Calories, a
total of 6000 Calories. The second Elf is carrying one food item with
4000 Calories. The third Elf is carrying food with 5000 and 6000
Calories, a total of 11000 Calories. The fourth Elf is carrying food
with 7000, 8000, and 9000 Calories, a total of 24000 Calories. The fifth
Elf is carrying one food item with 10000 Calories. In case the Elves get
hungry and need extra snacks, they need to know which Elf to ask: they’d
like to know how many Calories are being carried by the Elf carrying the
most Calories. In the example above, this is `24000` (carried by the
fourth Elf).

Find the Elf carrying the most Calories. How many total Calories is that
Elf carrying?

# Solution

``` r
solve <- function(x) {
  result <- (x %>% mutate('elfid' = cumsum(is.na(x$V1))) %>% 
             group_by(elfid) %>% 
             summarise(food = sum(V1, na.rm = TRUE)) %>%
             slice(which.max(food)) %>%
             select(food))[1]
  return(result)
}
```

# Test

Start by loading test data then apply solve.

``` r
harness(24000, solve)
```

    ## [1] "Passed"

    ## # A tibble: 1 × 1
    ##    food
    ##   <int>
    ## 1 24000

# Answer

How many measurements are larger than the previous measurement?

Your puzzle answer was `67450`.

``` r
harness(67450, solve, FALSE)
```

    ## [1] "Passed"

    ## # A tibble: 1 × 1
    ##    food
    ##   <int>
    ## 1 67450
