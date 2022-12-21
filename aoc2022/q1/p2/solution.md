
# Helpers

    ## ── Attaching packages ─────────────────────────────────────── tidyverse 1.3.2 ──
    ## ✔ ggplot2 3.4.0      ✔ purrr   0.3.5 
    ## ✔ tibble  3.1.8      ✔ dplyr   1.0.10
    ## ✔ tidyr   1.2.1      ✔ stringr 1.5.0 
    ## ✔ readr   2.1.3      ✔ forcats 0.5.2 
    ## ── Conflicts ────────────────────────────────────────── tidyverse_conflicts() ──
    ## ✖ dplyr::filter() masks stats::filter()
    ## ✖ dplyr::lag()    masks stats::lag()

## Part Two

By the time you calculate the answer to the Elves’ question, they’ve
already realized that the Elf carrying the most Calories of food might
eventually run out of snacks.

To avoid this unacceptable situation, the Elves would instead like to
know the total Calories carried by the top three Elves carrying the most
Calories. That way, even if one of those Elves runs out of snacks, they
still have two backups.

In the example above, the top three Elves are the fourth Elf (with 24000
Calories), then the third Elf (with 11000 Calories), then the fifth Elf
(with 10000 Calories). The sum of the Calories carried by these three
elves is `45000`.

Find the top three Elves carrying the most Calories. How many Calories
are those Elves carrying in total?

# Solution

``` r
solve <- function(x) {
  result <- (x %>% mutate('elfid' = cumsum(is.na(x$V1))) %>% 
             group_by(elfid) %>% 
             summarise(food = sum(V1, na.rm = TRUE)) %>%
             arrange(desc(food)) %>%
             select(food))[1:3,]
  return(sum(result))
}
```

# Test

Start by loading test data then apply solve.

``` r
harness(45000, solve)
```

    ## [1] "Passed"

    ## [1] 45000

# Answer

Your puzzle answer was `199357`.

``` r
harness(199357, solve, FALSE)
```

    ## [1] "Passed"

    ## [1] 199357
