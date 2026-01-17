# Git Branching & Merging Example

The purpose of this assignment is to give you additional practice working with Git branches.

These notes will provide a refresher on how Git branches work: <https://notes.jpt.sh/guides/git.html#data-model>

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

Add the above to a file named `perftest.py`, and run it with `uv run python perftest.py`.

Take note of the output, we'll want to remember these numbers in the next step.

## Part 2. Exploring the Git History

Let's visualize the commit history concisely graph using: `git log --graph --oneline`

Our history begins at the bottom, with the most recent commit on top:

- `...` (HEAD -> main) TODO (final commit)
- `365e069` finished draft README
- `f3aa1fd` documentation for part 2
- `9f49e22` documentation for part 1
- `3dcc3d9` initial commit"

This is the history of our current branch, `main`.

Type `git branch` to see a list of branches, you'll see that there are two others: `pandas` and `polars`.

To see the entire history, let's add `--all` to our `git log`

`git log --graph --oneline --all`

```
* ... 
* f3aa1fd documentation for part 2
* 9f49e22 documentation for part 1
| * f314357 (pandas) pandas version
|/
| * 92b25a5 (polars) polars implementation
| * de76c5e add polars to project
|/
* 3dcc3d9 initial commit
```

The new commits that appear are branching off to the right:

```
| * f314357 (pandas) pandas version
|/
```

This is showing a branch named `pandas` with a single commit.

This is showing a branch named `polars` with two commits, the latest is `92b25a5`:

```
| * 92b25a5 (polars) polars implementation
| * de76c5e add polars to project
|/
```

The `(polars)` indicates where the head of the branch currently sits.

## Part 3. Perfomance Testing Pandas

Let's use `git switch` to move over to the latest commit on the `pandas` branch.

`git switch pandas`

**git switch**

- `git switch -c <branchname>` - creates a new branch
- `git switch <branchname>` - switches to an existing branch

To see the difference between this and the main branch, you can run `git diff main pay_gap.py`. The lines in red that begin with `-` are the lines removed from `main` and the lines in green with `+` are the new lines on this branch.

You'll see that the entire function was rewritten, while the beginning & end of the file are the same.

Once you've done that, run `uv run pytest` to ensure that the code works.

**It shouldn't!** `pandas` is not yet installed.

`uv add pandas`, and then run `uv run pytest` again.

Great, the same tests are passing with new code so we probably didn't break anything.

Now what about performance?

`uv run python perftest.py` won't work, because `perftest.py` isn't in our directory any more!

We didn't lose any work though, `perftest.py` is still sitting back on your `main` branch.

If we want to bring in the latest changes from `main` we need to do a `git merge`.

`git merge main --no-edit` will ask `git` to bring over all commits from `main` to the current branch. The `--no-edit` portion means that we want to use the default commit message. You can also add a custom message with `-m "message"` the same way you have with `git commit`.

You should see output that resembles:

```
Merge made by the 'ort' strategy.
README.md   | 176 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
perftest.py |  18 ++++++++
2 files changed, 190 insertions(+), 4 deletions(-)
create mode 100644 perftest.py 
```

Let's look at the commit graph:

```
*   e5f72b5 (HEAD -> pandas) Merge branch 'main' into pandas
|\
| * 3375e43 (main) perftest.py
| * 365e069 finished draft README
| * f3aa1fd documentation for part 2
| * 9f49e22 documentation for part 1
* | f314357 pandas version
|/
| * 92b25a5 (polars) polars implementation
| * de76c5e add polars to project
|/
* 3dcc3d9 initial commit    
```

At the top, you can see that a merge is a special kind of commit with multiple parents. My `e5f72b5` is the child of `3375e43` and `f314357` (your commit hashes will vary here).

Now we can run `uv run python perftest.py`!

Note these numbers and compare them to the numbers from before.
You should see a modest speed improvement over `csv`. `pandas` more efficient internal data structures that give it a speed advantage over equivaent python code in most cases.

Before proceeding, you'll want to make another commit on this branch for the changes you made to `pyproject.toml` and `uv.lock` when installing pandas.

```
git add pyproject.toml uv.lock
git commit -m "added pandas to pyproject"
git log --graph --oneline --all
```

What does your graph look like now?


## Part 4. Merging to main

Happy that we saw a speedup, we see no reason not to merge the `pandas` branch back into main.

To do that, you'll need to `git switch` back to main and `git merge` the `pandas` branch into it.

```
git switch main
git merge pandas
Updating 3375e43..6d5a6da
Fast-forward
 pay_gap.py     |  64 +++++++++++++--------------
 pyproject.toml |   1 +
 uv.lock        | 135 +++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 3 files changed, 167 insertions(+), 33 deletions(-)
```

This is a fast-forward merge. In the prior graph the label `main` was behind `pandas`, with a linear (non-branching) path between them. 

There is no need for two parents to bring `main` up to speed with `pandas`, if we look at the output of `git log --graph --oneline --all` we now see this:

```
* 6d5a6da (HEAD -> main, pandas) added pandas to pyproject
*   e5f72b5 Merge branch 'main' into pandas
|\
| * 3375e43 perftest.py
| * 365e069 finished draft README
| * f3aa1fd documentation for part 2
| * 9f49e22 documentation for part 1
* | f314357 pandas version
|/
| * 92b25a5 (polars) polars implementation
| * de76c5e add polars to project
|/
* 3dcc3d9 initial commit    
```

Here we see our most recent commit on `pandas` is also the  most recent commit on `main`, the `main` label has moved forward, but no new commit has been added.

It is possible for many branches to point to the same commit at a given moment in time. As soon as you make another commit (or merge) only the *active* branch will be moved forward.

If you ever lose track of your active branch, type `git branch` to see the current status.

## Part 5. `polars`

Polars is a newer dataframe library which is faster & has an API that is reminiscent of SQL that many people prefer.

We already have an implementation on the `polars` branch. Let's follow a similar process:

1. `git switch polars` to switch to the branch, look at `pay_gap.py` to confirm it now uses `polars`.
2. `uv run pytest` to ensure it works.
3. Before we can run the performance tests we need to bring over `perftest.py` again. This time however, the merge is going to be more complicated.

In Part 4, the only differences between the destination & source branch was the `perftest.py`, but now `main` has changed!

When we try to merge the branches we are notified that there are conflicts:

```
Auto-merging pay_gap.py
CONFLICT (content): Merge conflict in pay_gap.py
Auto-merging pyproject.toml
CONFLICT (content): Merge conflict in pyproject.toml
Auto-merging uv.lock
CONFLICT (content): Merge conflict in uv.lock
Automatic merge failed; fix conflicts and then commit the result.
```

This time, our git repository is left in a "broken" state. There were conflicting changes in these files and `git` isn't sure how to resolve them without our input.

Type `git status` to assess the damage:

```
On branch polars
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Changes to be committed:
        modified:   README.md
        new file:   perftest.py

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   pay_gap.py
        both modified:   pyproject.toml
        both modified:   uv.lock 
```

These changes are in our git index, the staging area. We haven't yet made a new commit.  Notice that `git merge --abort` will roll things back if we made a mistake here, but we'll push ahead.

First, open `pyproject.toml`, this is the simplest file and we can try to fix the issue there.

Within the file you'll notice this section:

```diff
dependencies = [
<<<<<<< HEAD
    "polars>=1.37.1",
=======
    "pandas>=2.3.3",
>>>>>>> main
    "pytest>=9.0.2",
]
```

This is the dreaded **merge conflict**, `git` has written both versions to the file for you to resolve.

The `<<<<<HEAD` line begins the section from the working branch (`polars` in our case), the `=======` line splits it from the other section, and `>>>>>main`  marks the bottom of the conflict.

Most likely this is no longer valid syntax for this kind of file!
**We'll need to remove those three lines before we're done here.**

Resolving a merge conflict requires picking between a few options:

1. Keep what's on the new branch: delete the lines from the other branch.
2. Keep what's on the old branch: delete the lines from this branch.
3. Something more complicated. Rarely, you'll want changes from both branches. This will require manually reviewing the differences and combining them. Attempting this without tests in place can be risky!

In this case, we want option 1. Remove the three marker lines and the `pandas` line.

Once you've resolved a conflict, add the file to your git index using `git add pyproject.toml`

This is helpful to keep track of which conflicts you've already resolved.

Next, open `pay_gap.py`, this file has two conflicts, one at the top of the file with the imports, and a second within the function.

Practice what we just did, and resolve these conflicts, picking the `polars` options in both cases.

Remember to `git add pay_gap.py` at the end of this step.

### resolving conflicts in uv.lock

You can open `uv.lock` and attempt to resolve conflicts in the same way, but given the size of this file it can be challenging.

Given the fact that `uv.lock` is generated from `pyproject.toml`, there's a simpler option:

```
rm uv.lock
uv sync
git add uv.lock
```

Once you are satisfied with fixes type `git status` and ensure that there are no unmerged files left. Then make a `git commit -m "merged main with polars"`

Now that we've resolved the conflicts, we can run `uv run python perftest.py`, and we should see that things are indeed far faster!

## Part 6. Merge to `main`?

You may say to yourself, now that we're convinced that `polars` is the right call for this work, we want to merge things back to main.

You may be concerned that this will cause a lot of merge conflicts as `main` still has the `pandas` code, and we'd essentially be resolving the same conflicts in reverse.

Let's try it:

```
$ git switch main
$ git merge polars
Updating 6d5a6da..2d2278a
Fast-forward
 pay_gap.py     |  41 ++++++++-------
 pyproject.toml |   2 +-
 uv.lock        | 153 ++++++++++----------------------------------------------
 3 files changed, 47 insertions(+), 149 deletions(-)
```

Fortunately, because `git` can see the merge history, it correcty identifies this as another fast-forward merge. It was able to see we'd already resolved these conflicts, and moved the `main` branch to where `polars` already was.

One more time, take a second to consider the state of `main`.

```
$ git log --graph --oneline --all
*   2d2278a (HEAD -> main, polars) merged main to polars
|\
| * 6d5a6da (pandas) added pandas to pyproject
| *   e5f72b5 Merge branch 'main' into pandas
| |\
| | * 3375e43 perftest.py
| | * 365e069 finished draft README
| | * f3aa1fd documentation for part 2
| | * 9f49e22 documentation for part 1
| * | f314357 pandas version
| |/
* | 92b25a5 polars implementation
* | de76c5e add polars to project
|/
* 3dcc3d9 initial commit
```

## Final Step. Cleaning Up

`git log` and `git branch` will still show the old branches, which we no longer need.

To delete a merged branch use `git branch -d <branchname>`.

This will only delete branches that are not completely merged into our current branch history, giving an error if not. (This can be overriden with `-D` instead, but be careful when deleting unmerged work!)

## Note About Data

earnings.csv is a copy of 'Monthly employment earnings' downloaded from <https://ilostat.ilo.org/data/> on January 13th 2026.

There are methodological differences between how countries collect this data that one should seriously consider in making head-to-head comparisons between different countries.

The example code in this assignment would merely be a starting point, helping to analyze trends and tease out potential anomalies & outliers in the data for further evaluation.

This is a good reminder that a real analysis requires more than simple manipulation of numbers, but taking time to carefully understand the nuances of your data and how it was collected.
