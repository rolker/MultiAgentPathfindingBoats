# Roadmap

Fork-only: this file is agent material and stays out of pull requests to
upstream.

## Direction

What must be true for the fork's current goal, each line with the check that
says whether it is true today. The sit-rep (`/agent-workspace:sitrep`) reads
this section and runs every check each time; the section holds no status.

**Acceptance case.** The functionality in this repository is used from a
ROS 2 package. In the owner's words (2026-11-18): "the goal is to be able to
use this functionality from a ROS 2 package that is stil TBD." The major
milestone: "having a solution where the code can be tested using a multi boat
simulator from unh_marine_simulation".

| Line | Check |
|------|-------|
| How to set this project up so code in a ROS 2 package can import the relevant modules is investigated and settled (#2) | `gh-issue 2 closed` |
| Whether ROS code is added to this repository or stays separate is decided (#3) | `gh-issue 3 closed` |
| A solution is tested with a multi-boat simulator from unh_marine_simulation (#4) | `gh-issue 4 closed` |
