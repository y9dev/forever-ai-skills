# Implementation plan

Order: T0 walking skeleton, then vertical slices by journey priority, then hardening.

| ID | Task (vertical slice) | Depends on | Role | Files / modules owned | Expected behavior | Acceptance (AC ids) | Required tests | Integration notes | Parallel group |
|----|-----------------------|------------|------|-----------------------|-------------------|---------------------|----------------|-------------------|----------------|
| T0 | Skeleton: app boots, DB migrates, 1 round trip, README run command | - | backend + frontend (sequential) | | | | smoke test | | - |
| T1 | | T0 | | | | | | | A |

Parallel groups: tasks with the same letter run concurrently only if their file sets are disjoint and the contract they share is frozen (reference doc + version).
Milestones (review points): after T<n>, T<m>.
Risks / sequencing notes:
