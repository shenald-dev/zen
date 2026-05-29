We are given a merge conflict in CHANGELOG.md between base (main) and head (PR branch).
 The ancestor is the common base.

 We are to perform a 3-way merge and output the resolved file.

 Steps:
 1. We note that the base (main) has a newer version (0.1.15) and the head (PR) has 0.1.14.
 2. The conflict is that both branches have added new version sections at the top.

 According to the rules:
   - We must keep ALL meaningful changes from both branches.
   - Since both branches modified the same part (the top of the changelog) by adding a new version section,
     we need to include both versions, but in the correct order (newest first).

 However, note that the base (main) has version 0.1.15 and the head (PR) has 0.1.14.
 Since 0.1.15 is newer than 0.1.14, the base's version should come first.

 But wait: the head branch (PR) is based on an older version of main? Actually, the ancestor had 0.1.13.
 Then:
   - base (main) added 0.1.14 and then 0.1.15? Actually, looking at the base version:
        ## [0.1.15] - 2026-05-28
        ... and then it has the old versions below.

   - head (PR) added 0.1.14 and then has the old versions (which include 0.1.13, etc.)

 However, note that the base (main) already has 0.1.15 and 0.1.14? Actually, let's look at the base version:

 Base (main) version:
   ## [0.1.15] - 2026-05-28
   ... (changes for 0.1.15)
   ## [0.1.14] - 2026-05-26   [This is present in base?]
   ... (changes for 0.1.14)
   ## [0.1.13] - 2026-05-22
   ... 

 But wait, the diff provided for base (main) in the context shows:

   Base (main): 
        # Changelog
        
      - ## [0.1.13] - 2026-05-22
      + ## [0.1.15] - 2026-05-28
        
        ### Changed
      - * **[Assurance]:** ... 
      + * **[Performance]:** ... 
      ... and so on.

 Actually, the base (main) version in the context shows that it replaced the 0.1.13 section with 0.1.15 and then
 added some changes and then kept the old 0.1.12, etc. But note that the base version also has a 0.1.14 section?

 Let me re-read the context for base (main):

   Base (main): 83 lines changed (lines 3-100)
        # Changelog
        
      - ## [0.1.13] - 2026-05-22
      + ## [0.1.15] - 2026-05-28
        
        ### Changed
      - * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
      + * **[Performance]:** Moved early exit condition (`remaining <= 0`) to the top of the timer loop to avoid redundant elapsed time calculations and unnecessary UI update attempts.
      - * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.
      + * **[Maintainability]:** Removed redundant `min(elapsed, seconds)` checks during UI refresh since `elapsed` is inherently bounded by the loop structure.
      - 
      + * **[Reliability]:** Hardened the `KeyboardInterrupt` terminal cleanup handler with an explicit `console is not None` check to prevent ambiguity and ensure robust posix 130 exits.
      - ## [0.1.12] - 2026-05-21
      + * **[Release]:** Cut release v0.1.15 to formalize the lifecycle assessment and finalize codebase stabilization.
        
      - ### Changed
      + ## [0.1.14] - 2026-05-26
      - * **[Reliability]:** Addressed an edge case where floating-point drift could cause the calculated sleep duration to evaluate to a negative number, resulting in a `ValueError`. Guarded `time.sleep()` with a bounds check (`max(0, ...)`).
      + 
      - * **[Release]:** Cut release v0.1.12 to finalize stability improvements.
      + ### Changed
      - 
      + * **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.
      - ## [0.1.11] - 2026-05-20
      + * **[Release]:** Cut release v0.1.14 to formalize the lifecycle assessment and finalize codebase stabilization.
        
      - ### Changed
      + ## [0.1.13] - 2026-05-22
      - * **[Assurance]:** Validated test suite fix for infinite loops caused by time.monotonic mocks and rich background threads. Ensured robust stateful mocking pattern is used.
      + 
      - * **[Maintenance]:** Fixed out-of-order changelog entries.
      + ### Changed
      - * **[Release]:** Cut release v0.1.11 to finalize codebase stabilization.
      + * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
      - 
      + * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.
      - ## [0.1.10] - 2026-04-16
      + 
      - 
      + ## [0.1.12] - 2026-05-21
      - ### Changed
      + 
      - * **[Assurance]:** Validated codebase structural integrity, ran adversarial QA, and ensured testing and static analysis fully pass. No regressions found after previous agent codebase maintenance.
      + ### Changed
      - * **[Release]:** Cut release v0.1.10 to formalize the lifecycle assessment and finalize codebase stabilization.
      + * **[Reliability]:** Addressed an edge case where floating-point drift could cause the calculated sleep duration to evaluate to a negative number, resulting in a `ValueError`. Guarded `time.sleep()` with a bounds check (`max(0, ...)`).
      - 
      + * **[Release]:** Cut release v0.1.12 to finalize stability improvements.
        
      - ## [0.1.9] - 2026-04-15
      + ## [0.1.11] - 2026-05-20
        
        ### Changed
      - * **[Maintainability]:** Removed redundant module docstring in `timer.py`.
      + * **[Assurance]:** Validated test suite fix for infinite loops caused by time.monotonic mocks and rich background threads. Ensured robust stateful mocking pattern is used.
      - * **[Maintainability]:** Excluded `.pytest_cache/` in `.gitignore`.
      + * **[Maintenance]:** Fixed out-of-order changelog entries.
      - * **[Maintainability]:** Explicitly omitted execution files from test coverage tracking.
      + * **[Release]:** Cut release v0.1.11 to finalize codebase stabilization.
        
      - ## [0.1.8] - 2026-04-11
      + ## [0.1.10] - 2026-04-16
        
        ### Changed
      - * **[Assurance]:** Validated stability of the recent changes.
      + * **[Assurance]:** Validated codebase structural integrity, ran adversarial QA, and ensured testing and static analysis fully pass. No regressions found after previous agent codebase maintenance.
      - * **[UI]:** Allow the progress bar to dynamically resize by setting `bar_width=None`. Add a visual/audible terminal bell via `console.bell()` upon session completion.
      + * **[Release]:** Cut release v0.1.10 to formalize the lifecycle assessment and finalize codebase stabilization.
      - * **[Release]:** Cut release v0.1.8.
      + 
        
      - ## [0.1.7] - 2026-04-05
      + ## [0.1.9] - 2026-04-15
        
        ### Changed
      - * **[Assurance]:** Validated stability of the timer loop optimization that removed redundant time recalculations. No functional regressions were detected.
      + * **[Maintainability]:** Removed redundant module docstring in `timer.py`.
      - * **[Release]:** Cut release v0.1.7 to formalize the lifecycle assessment and finalize codebase stabilization.
      + * **[Maintainability]:** Excluded `.pytest_cache/` in `.gitignore`.
      - 
      + * **[Maintainability]:** Explicitly omitted execution files from test coverage tracking.

 This is very messy. It appears that the base (main) branch has done a lot of reordering and version bumping.

 However, note the Git Diff (Head changes vs base) provided:

   @@ -1,5 +1,12 @@
    # Changelog
    
   +## [0.1.14] - 2026-05-26
   +
   +### Changed
   +* **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.
   +* **[Assurance]:** Validated codebase structural integrity. Static analysis and test suite execution yielded zero errors and 100% coverage. No dead code or architectural vulnerabilities were found. Entropy is stable.
   +* **[Release]:** Cut release v0.1.14 to formalize the lifecycle assessment and finalize codebase stabilization.
   +
    ## [0.1.13] - 2026-05-22
    
    ### Changed

 This diff shows that the head branch (PR) has added a new section for 0.1.14 at the top, and then the base (main) 
 version (which we are merging into) currently has 0.1.13 at the top? But wait, the base (main) version in the context 
 actually has 0.1.15 at the top.

 How to resolve?

 Let's think about the actual states:

 Ancestor: 
   ## [0.1.13] - 2026-05-22
   ... (then the old versions)

 Base (main): 
   It has:
      ## [0.1.15] - 2026-05-28
      ... (changes for 0.1.15)
      ## [0.1.14] - 2026-05-26   [This is present in base?]
      ... (changes for 0.1.14)
      ## [0.1.13] - 2026-05-22
      ... (and then the rest)

 But wait, the context for base (main) shows that it replaced the 0.1.13 section with 0.1.15 and then inserted 0.1.14? 
 Actually, the base (main) context shows:

   - ## [0.1.13] - 2026-05-22   [removed]
   + ## [0.1.15] - 2026-05-28   [added]

   and then later:

   - ## [0.1.12] - 2026-05-21   [removed?]
   + ## [0.1.14] - 2026-05-26   [added]

   and then:

   - ## [0.1.11] - 2026-05-20   [removed?]
   + ## [0.1.13] - 2026-05-22   [added]

   and so on.

 This suggests that the base (main) branch has done a version bump from 0.1.13 to 0.1.15, and in the process 
 inserted 0.1.14 and 0.1.13 as previous versions? Actually, it looks like they are shifting the versions down.

 However, note that the head branch (PR) has:

   ## [0.1.14] - 2026-05-26
   ... (changes for 0.1.14)
   ## [0.1.13] - 2026-05-22
   ... (then the old versions)

 So the head branch (PR) is adding a 0.1.14 version on top of the ancestor (which had 0.1.13).

 The base (main) branch has added 0.1.15 and 0.1.14 (and then 0.1.13, etc.) on top of the ancestor.

 Therefore, when merging, we want:

   [0.1.15] (from base)
   [0.1.14] (from base? but note: the head also has 0.1.14) -> we must avoid duplication.

 However, the changes in 0.1.14 between base and head are different.

 Let's look at the changes for 0.1.14 in base (main) and in head (PR):

 Base (main) for 0.1.14 (from the context):

      ## [0.1.14] - 2026-05-26

        ### Changed
      - * **[Reliability]:** Addressed an edge case where floating-point drift could cause the calculated sleep duration to evaluate to a negative number, resulting in a `ValueError`. Guarded `time.sleep()` with a bounds check (`max(0, ...)`).
      + 
      - * **[Release]:** Cut release v0.1.12 to finalize stability improvements.
      + ### Changed
      - 
      + * **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.

   This seems to be a mess of conflict markers? Actually, the context provided for base (main) is showing the diff 
   between ancestor and base? But it's presented as the base version.

   Alternatively, let's look at the Git Diff (Head changes vs base) which is the diff of the head branch against the base.

   That diff shows that the head branch has added a 0.1.14 section that is not in the base.

   Therefore, the base branch does not have the 0.1.14 section that the head branch has? 

   But wait, the base (main) context shows that it has a 0.1.14 section? 

   Actually, the base (main) context shows:

        - ## [0.1.12] - 2026-05-21
        + ## [0.1.14] - 2026-05-26

   meaning that in the base branch, the 0.1.12 section was replaced by a 0.1.14 section? 

   This is confusing.

 Let me try to reconstruct:

   Ancestor had:
        ## [0.1.13] - 2026-05-22
        ## [0.1.12] - 2026-05-21
        ## [0.1.11] - 2026-05-20
        ... 

   Base (main) changed it to:
        ## [0.1.15] - 2026-05-28
        ## [0.1.14] - 2026-05-26
        ## [0.1.13] - 2026-05-22
        ## [0.1.12] - 2026-05-21   [but wait, the context shows that the 0.1.12 was replaced by 0.1.14?]

   Actually, the base (main) context shows:

        - ## [0.1.13] - 2026-05-22   -> removed
        + ## [0.1.15] - 2026-05-28   -> added

        then later:

        - ## [0.1.12] - 2026-05-21   -> removed
        + ## [0.1.14] - 2026-05-26   -> added

        and then:

        - ## [0.1.11] - 2026-05-20   -> removed
        + ## [0.1.13] - 2026-05-22   -> added

   So the base (main) branch has:

        [0.1.15]
        [0.1.14]
        [0.1.13]   (which was the old [0.1.11]?)
        [0.1.12]   (which was the old [0.1.10]?) ... 

   This doesn't make sense.

 Given the complexity, let's rely on the Git Diff (Head changes vs base) and the fact that we are to keep all changes.

 The Git Diff (Head changes vs base) shows:

   The head branch has added a new section at the top for 0.1.14 (with specific changes) and then the base version 
   (which we are merging into) has the 0.1.13 section at the top? 

   But wait, the base (main) version in the context actually has 0.1.15 at the top? 

   The Git Diff (Head changes vs base) is showing the difference between the head branch and the base branch.

   It says:

        @@ -1,5 +1,12 @@
         # Changelog
         
        +## [0.1.14] - 2026-05-26
        +
        +### Changed
        +* **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.
        +* **[Assurance]:** Validated codebase structural integrity. Static analysis and test suite execution yielded zero errors and 100% coverage. No dead code or architectural vulnerabilities were found. Entropy is stable.
        +* **[Release]:** Cut release v0.1.14 to formalize the lifecycle assessment and finalize codebase stabilization.
        +
         ## [0.1.13] - 2026-05-22
         
         ### Changed

   This means that in the base branch, the file starts with:

        # Changelog

        ## [0.1.13] - 2026-05-22

        ### Changed

   and the head branch has:

        # Changelog

        ## [0.1.14] - 2026-05-26

        ### Changed
        * [Reliability]: ... 
        * [Assurance]: ...
        * [Release]: ...

        ## [0.1.13] - 2026-05-22

        ### Changed

   However, we know from the context that the base (main) branch actually has a 0.1.15 and 0.1.14? 

   This suggests that the Git Diff (Head changes vs base) is not showing the entire base branch state, but only the 
   part that is in conflict? 

   But the problem says: "Git Diff (Head changes vs base)" and it shows a diff that starts at line 1.

   Alternatively, the base branch might have been updated to 0.1.15, but the conflict is only in the top part? 

   Let me read the context again:

        Base (main): 83 lines changed (lines 3-100)

   and

        Head (jules-5676753565371360900-7fdd35c3): 73 lines changed (lines 3-93)

   So the changes are in the same line range (starting at line 3). 

   The Git Diff (Head changes vs base) shows:

        @@ -1,5 +1,12 @@

   meaning that in the base branch, lines 1-5 are:

        1: # Changelog
        2: 
        3: ## [0.1.13] - 2026-05-22
        4: 
        5: ### Changed

   and in the head branch, lines 1-12 are:

        1: # Changelog
        2: 
        3: ## [0.1.14] - 2026-05-26
        4: 
        5: ### Changed
        6: * **[Reliability]:** ...
        7: * **[Assurance]:** ...
        8: * **[Release]:** ...
        9: 
        10: ## [0.1.13] - 2026-05-22
        11: 
        12: ### Changed

   Therefore, the base branch at the top has the 0.1.13 section, and the head branch has added a 0.1.14 section on top.

   But wait, the context for base (main) said that it had changed the 0.1.13 to 0.1.15? 

   This implies that the base (main) branch has actually changed beyond the lines shown in the diff? 

   However, the problem states that the base (main) has 83 lines changed (lines 3-100). The Git Diff (Head changes vs base) 
   only shows the first 5 lines of the base branch? 

   This suggests that the base branch has changes throughout the file, but the conflict we are seeing in the diff is only 
   at the very top.

   How to resolve?

   We are told to keep all changes from both branches.

   The head branch has added a 0.1.14 section at the top.

   The base branch has, according to the context, changed the top section to 0.1.15 and then made other changes 
   throughout the file (including inserting 0.1.14 and 0.1.13 in the history?).

   But note: the Git Diff (Head changes vs base) shows that the base branch at the top has 0.1.13. 

   This is a contradiction.

   Let me look at the provided file versions:

   Ancestor (common base): 
        # Changelog

        ## [0.1.13] - 2026-05-22

        ... (then the rest)

   Base (main) — target branch:
        # Changelog

        ## [0.1.15] - 2026-05-28

        ... (then the rest)

   Head (jules-5676753565371360900-7fdd35c3) — PR branch:
        # Changelog

        ## [0.1.14] - 2026-05-26

        ... (then the rest)

   So the base branch has 0.1.15 at the top, and the head branch has 0.1.14 at the top.

   The Git Diff (Head changes vs base) must be wrong? Or perhaps it is showing the diff after the base branch 
   has been updated? 

   But the problem says: "Git Diff (Head changes vs base)".

   Alternatively, the base branch might have been updated to 0.1.15, but