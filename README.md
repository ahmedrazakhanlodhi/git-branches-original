# Git Branching & Merging Example

The purpose of this assignment is to give you additional practice working with Git branches.

Git branches allow us to have parallel histories, versions of files that we haven't yet decided we'd like to be part of our work's history.

TODO: explanation or use old notes?

## Part 1. Introduction

`pay_gap.py` is a small program that analyzes pay equality using the provided `earnings.csv`.

If you run the program you'll see a table of the top gender pay gaps represented in the data.

You can also run `uv run pytest` to check that the program is returning the
expected results.

The program uses the built-in `csv` module, where many might prefer `pandas` or `polars`. The code is clear enough, but we're curious about performance.

Let's write a small performance test using Python's built-in `timeit` module:

```
# perftest.py
import timeit
from pay_gap import get_top_pay_disparities


if __name__ == "__main__":
    number = 100
    
    elapsed = timeit.timeit(
        lambda: get_top_pay_disparities(10),
        number=number
    )
    
    avg_time = elapsed / number
    
    print(f"Total time:   {elapsed:.4f} seconds")
    print(f"Average time: {avg_time:.4f} seconds")
    print(f"Per call:     {avg_time * 1000:.2f} ms")
```

Add the above to a file named `perftest.py`, and run it with `uv run perftest.py`.

Take note of the output, we'll want to remember these numbers in the next step.

## Part 2. Exploring the Git History

TODO: how to visualize?

Let's visualize the graph using: `git log --graph --oneline`

Our history begins at the bottom, with the most recent commit on top:

- `` documentation for part 2
- `9f49e22` documentation for part 1
- `3dcc3d9` initial commit"

This is the history of our current branch, `main`.

Type `git branch` to see a list of branches, you'll see that there are two others: `pandas` and `polars`.

To see the entire history, let's add `--all` to our `git log`

`git log --graph --oneline --all`

```
TODO: final  
```

Here we see that there are commits that split off the main trunk:

- `92b25a5` **(polars)** polars implementation
- `de76c5e` add polars to project

The `(polars)` indicates where the head of the branch currently sits.

## Part 3. Perfomance Testing Pandas

- `git switch -c <branchname>` - creates a new branch
- `git switch <branchname>` - switches to an existing branch

Let's use `git switch` to move over to the latest commit on the `pandas` branch.

Once you've done that, run `uv run`

## Note About Data

earnings.csv is a copy of 'Monthly employment earnings' downloaded from <https://ilostat.ilo.org/data/> on January 13th 2026.

There are methodological differences between how countries collect this data that one should seriously consider in making head-to-head comparisons between different countries.

The example code in this assignment would merely be a starting point, helping to analyze trends and tease out potential anomalies & outliers in the data for further evaluation.

This is a good reminder that a real analysis requires more than simple manipulation of numbers, but taking time to carefully understand the nuances of your data and how it was collected.
