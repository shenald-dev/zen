We are given a merge conflict in CHANGELOG.md between base (main) and head (PR branch) with a common ancestor.

The goal is to produce a resolved file that includes all meaningful changes from both branches.

From the context:

- The base branch (main) has changes that include:
  - Updating the version from [0.1.13] to [0.1.14] at the top (with date 2026-05-26)
  - Then, for each version section, it has updated the version numbers and dates (shifting down) and updated the bullet points under "### Changed" for each version.

- The head branch (PR branch) has changes that include:
  - Also updating the version from [0.1.13] to [0.1.14] at the top (with date 2026-05-26)
  - But then, for the [0.1.14] section, it has a different set of bullet points under "### Changed":
        * **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.
        * **[Assurance]:** Validated codebase structural integrity. Static analysis and test suite execution yielded zero errors and 100% coverage. No dead code or architectural vulnerabilities were found. Entropy is stable.
        * **[Release]:** Cut release v0.1.14 to formalize the lifecycle assessment and finalize codebase stabilization.

  - For the subsequent versions, the head branch has shifted the version numbers and dates (like the base) but with different bullet points.

However, note that the base branch also has changes for the subsequent versions (from [0.1.13] down to [0.1.7]) and the head branch has changes for the same set of versions.

But observe: the base branch and head branch both have the same version header for [0.1.14] at the top, but different content under "### Changed" for that version.

For the other versions (like [0.1.13], [0.1.12], etc.), both branches have updated the version numbers and dates (so they are in sync in terms of which version is which) but the bullet points under "### Changed" are different.

How to resolve:

1. For the [0.1.14] section:
   - Base branch has:
        * **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.
        * **[Release]:** Cut release v0.1.14 to formalize the lifecycle assessment and finalize codebase stabilization.
   - Head branch has:
        * **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.
        * **[Assurance]:** Validated codebase structural integrity. Static analysis and test suite execution yielded zero errors and 100% coverage. No dead code or architectural vulnerabilities were found. Entropy is stable.
        * **[Release]:** Cut release v0.1.14 to formalize the lifecycle assessment and finalize codebase stabilization.

   We note that the Reliability and Release bullets are the same in both. The head branch has an extra Assurance bullet.

   According to rule 2: Keep ALL meaningful changes from BOTH branches.

   Therefore, for [0.1.14] we should include:
        * **[Reliability]:** ... (same in both)
        * **[Assurance]:** ... (from head)
        * **[Release]:** ... (same in both)

   But note: the base branch does not have the Assurance bullet, and the head branch does. So we add the Assurance bullet from head.

   However, we must check if the base branch has any other bullet in [0.1.14] that the head doesn't? The base branch only has two bullets (Reliability and Release) and the head has three (Reliability, Assurance, Release). So we take the three.

2. For the other versions (like [0.1.13], [0.1.12], etc.):

   We see that both branches have changed the version numbers and dates (so the structure of the changelog is the same: each version section is present and in the same order). However, the bullet points under "### Changed" for each version are different.

   Example for [0.1.13]:

   Base branch:
        ### Changed
        * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
        * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.

   Head branch:
        ### Changed
        * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
        * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.

   Wait, actually in the provided diff for the head branch, we see that for [0.1.13] the head branch has:

        ## [0.1.13] - 2026-05-22

        ### Changed
        * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
        * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.

   But wait, the base branch for [0.1.13] is:

        ## [0.1.13] - 2026-05-22

        ### Changed
        * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
        * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.

   They look the same? However, looking at the context description:

   Base (main) for [0.1.13]:
        - * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
        + * **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.
        - * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.
        + * **[Release]:** Cut release v0.1.14 to formalize the lifecycle assessment and finalize codebase stabilization.

   This seems to be a diff of the base branch relative to the ancestor? Actually, the context provided is a bit confusing.

   Let me re-read the context:

   The context says for base (main): 68 lines changed (lines 3-92) and then shows a diff. But note: the diff shown in the context for base (main) is actually the diff from the ancestor to base? Or is it the current state of base?

   Actually, the context says:

   **Base (main):** The target branch (has newer changes from others)

   And then it shows:

        # Changelog
        
      - ## [0.1.13] - 2026-05-22
      + ## [0.1.14] - 2026-05-26
        
          ### Changed
      - * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
      + * **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.
      - * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.
      + * **[Release]:** Cut release v0.1.14 to formalize the lifecycle assessment and finalize codebase stabilization.
        
      - ## [0.1.12] - 2026-05-21
      + ## [0.1.13] - 2026-05-22
        
          ### Changed
      - * **[Reliability]:** Addressed an edge case where floating-point drift could cause the calculated sleep duration to evaluate to a negative number, resulting in a `ValueError`. Guarded `time.sleep()` with a bounds check (`max(0, ...)`).
      + * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
      - * **[Release]:** Cut release v0.1.12 to finalize stability improvements.
      + * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.
        
      ... and so on.

   This is actually showing the changes that base (main) made relative to the ancestor? But note: the ancestor had [0.1.13] as the latest? Then base (main) changed it to [0.1.14] and shifted everything down.

   Similarly, the head branch context shows:

        # Changelog
        
      - ## [0.1.13] - 2026-05-22
      + ## [0.1.14] - 2026-05-26
        
          ### Changed
      - * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
      + * **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.
      - * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.
      + * **[Assurance]:** Validated codebase structural integrity. Static analysis and test suite execution yielded zero errors and 100% coverage. No dead code or architectural vulnerabilities were found. Entropy is stable.
      -  
      + * **[Release]:** Cut release v0.1.14 to formalize the lifecycle assessment and finalize codebase stabilization.
        
      - ## [0.1.12] - 2026-05-21
      +  
      -  
      + ## [0.1.13] - 2026-05-22
      - ### Changed
      +  
      - * **[Reliability]:** Addressed an edge case where floating-point drift could cause the calculated sleep duration to evaluate to a negative number, resulting in a `ValueError`. Guarded `time.sleep()` with a bounds check (`max(0, ...)`).
      + ### Changed
      - * **[Release]:** Cut release v0.1.12 to finalize stability improvements.
      + * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
      -  
      + * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.
        
      ... and so on.

   This is showing the changes that the head branch made relative to the ancestor? But note: the head branch also changed the top version to [0.1.14] and then has some differences in the bullet points.

   However, we are also given the actual file versions for base and head (with truncation) and the git diff (head changes vs base).

   The git diff (head changes vs base) is:

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
        @@ -82,4 +89,4 @@
         * **[Performance]:** Disabled the `rich` secondary background thread for rendering. Handled manual synchronous UI refreshes directly from the main process event loop. This zeroes out background context switching and thread contention.
         * **[Pruned]:** Removed an unused `pytest` import from the test suite.
         * **[Dependencies]:** Bumped minimum dependency baselines to `rich>=13.9.0` and `typer>=0.12.0`.
        -* **[Testing]:** Added missing test coverage for the root CLI app module execution path.
        +* **[Testing]:** Added missing test coverage for the root CLI app module execution path.
        \ No newline at end of file

   This diff shows that the head branch (compared to base) has:

   - Added a new section at the top for [0.1.14] (with three bullets: Reliability, Assurance, Release)
   - And then the rest of the file is the same as base? Except for the last line: the base had a newline at the end? Actually, the diff shows that the base had a newline at the end of the file (because the line is unchanged except for the addition of a backslash and "No newline at end of file" in the diff header? Actually, the diff says:

        -* **[Testing]:** Added missing test coverage for the root CLI app module execution path.
        +* **[Testing]:** Added missing test coverage for the root CLI app module execution path.
        \ No newline at end of file

   This means that the base branch had a newline at the end of the file, and the head branch does not? But the diff shows the same line of text, so the only difference is the missing newline.

   However, note: the diff header says "\\ No newline at end of file", meaning that the head branch is missing the newline that the base branch had.

   But wait: the base branch version (as given in the context) ends with:

        * **[Testing]:** Added missing test coverage for the root CLI app module execution path.

   and then presumably a newline? The head branch version (as given) ends with the same line but without a newline.

   However, the conflict resolution should not worry about the newline at the end of file? We are to output the resolved file content.

   Now, the key point from the git diff: the head branch (PR) has added a new top section for [0.1.14] (with three bullets) and then the rest of the file is identical to the base branch? But wait, the base branch already had a [0.1.14] section at the top? 

   Let me clarify:

   The base branch (main) as given in the context starts with:

        # Changelog

        ## [0.1.14] - 2026-05-26

        ### Changed
        * **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.
        * **[Release]:** Cut release v0.1.14 to formalize the lifecycle assessment and fina

   ... and then the rest.

   The head branch (PR) as given in the context starts with:

        # Changelog

        ## [0.1.14] - 2026-05-26

        ### Changed
        * **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.
        * **[Assurance]:** Validated codebase structural integrity. Static analysis and test suite execution yielded zero errors and 100% coverage. No dead code or architectural vulnerabilities were found. Entropy is stable.
        * **[Release]:** Cut release v0.1.14 to formalize the lifecycle assessment and finalize codebase stabilization.

   ... and then the rest.

   So the base branch has two bullets under [0.1.14] and the head branch has three.

   The git diff (head vs base) shows that the head branch has, relative to base, added:

        ## [0.1.14] - 2026-05-26

        ### Changed
        * **[Reliability]:** ... (same as base's first bullet)
        * **[Assurance]:** ... (new)
        * **[Release]:** ... (same as base's second bullet)

   and then the rest of the file is the same? But wait, the base branch already had a [0.1.14] section? So why is the diff showing an addition of the entire [0.1.14] section?

   This suggests that the base branch, as we are seeing it in the context, does not actually have the [0.1.14] section? But that contradicts the context.

   Alternatively, the context provided for base and head might be the entire file? And the git diff is showing the difference between head and base.

   Let's look at the git diff again: it shows that head has, compared to base, an addition of 7 lines at the top (from line 1 to 5 becoming 1 to 12) and then a change at the end (the last line).

   This implies that the base branch does not have the [0.1.14] section at the top? But that can't be because the context says base has:

        ## [0.1.14] - 2026-05-26

   at the top.

   Unless the base branch context provided is not the entire file? But it says it's truncated.

   Another possibility: the base branch and head branch both have the [0.1.14] section, but they are different? And the git diff is showing that the head branch has changed the [0.1.14] section? But the diff shows an addition, not a change.

   Actually, the diff shows:

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

   This means that in the base branch, the first 5 lines were:

        # Changelog
        
        ## [0.1.13] - 2026-05-22

   and in the head branch, the first 12 lines are:

        # Changelog
        
        ## [0.1.14] - 2026-05-26
        
        ### Changed
        * **[Reliability]:** ...
        * **[Assurance]:** ...
        * **[Release]:** ...

   So the base branch, as we are seeing it in the git diff, does not have the [0.1.14] section? It has [0.1.13] as the top section.

   This contradicts the context that said base (main) has:

        ## [0.1.14] - 2026-05-26

   at the top.

   But note: the context said for base (main): "68 lines changed (lines 3-92)" and then showed a diff that started with:

        # Changelog
        
      - ## [0.1.13] - 2026-05-22
      + ## [0.1.14] - 2026-05-26

   This diff is from the ancestor to base. So the ancestor had [0.1.13] at the top, and base changed it to [0.1.14].

   Similarly, the head branch context showed a diff from ancestor to head that also changed the top to [0.1.14].

   Therefore, both base and head have changed the top version from [0.1.13] (in the ancestor) to [0.1.14]. But they have different content under the [0.1.14] section.

   And the git diff (head vs base) shows that relative to base, the head branch has:

        - Changed the top section from [0.1.13] to [0.1.14] (but wait, base already has [0.1.14]? So why is the diff showing an addition of [0.1.14]?)

   Let me try to reconstruct:

   Ancestor:
        # Changelog
        
        ## [0.1.13] - 2026-05-22
        ... (rest of the changelog for older versions)

   Base (main):
        # Changelog
        
        ## [0.1.14] - 2026-05-26   [changed from [0.1.13]]
        ### Changed
        * [Reliability]: ... 
        * [Release]: ...
        ## [0.1.13] - 2026-05-22   [this is the old top, now moved down]
        ... (the rest, but with version numbers shifted up by one? Actually, the context shows that base changed every version: [0.1.13] became [0.1.14], [0.1.12] became [0.1.13], etc.)

   Head (PR):
        # Changelog
        
        ## [0.1.14] - 2026-05-26   [changed from [0.1.13]]
        ### Changed
        * [Reliability]: ... 
        * [Assurance]: ...   (new)
        * [Release]: ...
        ## [0.1.13] - 2026-05-22   [old top, moved down]
        ... (but with different bullet points for the old versions)

   Now, the git diff (head vs base) is comparing the head branch to the base branch.

   In the base branch, the file starts with:

        # Changelog
        
        ## [0.1.14] - 2026-05-26
        ### Changed
        * [Reliability]: ... 
        * [Release]: ...
        ## [0.1.13] - 2026-05-22
        ...

   In the head branch, the file starts with:

        # Changelog
        
        ## [0.1.14] - 2026-05-26
        ### Changed
        * [Reliability]: ... 
        * [Assurance]: ... 
        * [Release]: ...
        ## [0.1.13] - 2026-05-22
        ...

   So the difference is that in the head branch, under the [0.1.14] section, there is an extra bullet point for Assurance.

   Therefore, the git diff should show:

        @@ -1,8 +1,11 @@
         # Changelog
         
         ## [0.1.14] - 2026-05-26
         ### Changed
        -* **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.
        -* **[Release]:** Cut release v0.1.14 to formalize the lifecycle assessment and finalize codebase stabilization.
        +* **[Reliability]:** Capped all open-ended top-level and development dependencies in `pyproject.toml` with safe upper major version bounds to prevent unexpected build failures from future breaking upstream releases.
        +* **[Assurance]:** Validated codebase structural integrity. Static analysis and test suite execution yielded zero errors and 100% coverage. No dead code or architectural vulnerabilities were found. Entropy is stable.
        +* **[Release]:** Cut release v0.1.14 to formalize the lifecycle assessment and finalize codebase stabilization.
         ## [0.1.13] - 2026-05-22

   But the provided git diff is:

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

   This suggests that the base branch, in the git diff, does not have the [0.1.14] section at all? It has the [0.1.13] section as the top.

   This is confusing.

   However, note the git diff says: "Head changes vs base", meaning we are taking the base as the old and head as the new.

   And the diff shows that head has, compared to base, added a block of 7 lines (from line 1 to 5 becoming 1 to 12) and then a change at the end.

   Given the confusion, let's rely on the provided file versions for base and head (even though truncated) and the resolution rules.

   We know:

   - Both branches have a [0.1.14] section at the top.
   - The base branch's [0.1.14] section has two bullets: Reliability and Release.
   - The head branch's [0.1.14] section has three bullets: Reliability, Assurance, and Release.

   For the rest of the file (the older versions), we see that both branches have shifted the version numbers (so the structure is the same) but the bullet points are different.

   How to resolve the older versions?

   We must keep all meaningful changes from both branches.

   Example for [0.1.13]:

   Base branch has:
        ### Changed
        * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
        * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.

   Head branch has:
        ### Changed
        * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
        * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.

   Wait, they look identical? But the context description showed differences.

   Let me look at the context for base (main) for [0.1.13]:

        - ## [0.1.12] - 2026-05-21
        + ## [0.1.13] - 2026-05-22
        
            ### Changed
        - * **[Reliability]:** Addressed an edge case where floating-point drift could cause the calculated sleep duration to evaluate to a negative number, resulting in a `ValueError`. Guarded `time.sleep()` with a bounds check (`max(0, ...)`).
        + * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
        - * **[Release]:** Cut release v0.1.12 to finalize stability improvements.
        + * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.

   This is showing that in the base branch, the [0.1.13] section (which was [0.1.12] in the ancestor) has been changed from:
        * [Reliability]: ... 
        * [Release]: Cut release v0.1.12 ...
   to:
        * [Assurance]: ... 
        * [Release]: Cut release v0.1.13 ...

   Similarly, for the head branch, the context shows for [0.1.13]:

        - ## [0.1.12] - 2026-05-21
        +  
        -  
        + ## [0.1.13] - 2026-05-22
        - ### Changed
        +  
        - * **[Reliability]:** Addressed an edge case where floating-point drift could cause the calculated sleep duration to evaluate to a negative number, resulting in a `ValueError`. Guarded `time.sleep()` with a bounds check (`max(0, ...)`).
        + ### Changed
        - * **[Release]:** Cut release v0.1.12 to finalize stability improvements.
        + * **[Assurance]:** Validated codebase structural integrity and implemented an adversarial QA test simulating extreme floating-point drift to guarantee the `max(0, ...)` bounds logic for `time.sleep()` flawlessly prevents exceptions.
        -  
        + * **[Release]:** Cut release v0.1.13 to formalize the lifecycle assessment and finalize codebase stabilization.

   This is showing that in the head branch, the [0.1.13] section (which was [0.1.12] in the ancestor) has been changed from:
        * [Reliability]: ... 
        * [Release]: Cut release v0.1.12 ...
   to:
        * [Assurance]: ... 
        * [Release]: Cut release v0.1.13 ...

   So both branches have the same change for the [0.1.13] section? They both replaced the Reliability bullet with an Assurance bullet and updated the release version.

   But wait, the base branch context showed for [0.1.13]:
        * [Assurance]: ... 
        * [Release]: Cut release v0.1.13 ...

   and the head branch context showed for [0.1.13]:
        * [Assurance]: ... 
        * [Release]: Cut release v0.1.13 ...

   So they are the same.

   However, let's check another version, say [0.1.12]:

   Base branch context:
        - ## [0.1.11] - 2026-05-20
        + ## [0.1.12] - 2026-05-21
        
            ### Changed
        - * **[Assurance]:** Validated test suite fix for infinite loops caused by time.monotonic mocks and rich background threads. Ensured robust stateful mocking pattern is used.
        + * **[Reliability]:** Addressed an edge case where floating-point drift could cause the calculated sleep duration to evaluate to a negative number, resulting in a `ValueError`. Guarded `time.sleep()` with a bounds check (`max(0, ...)`).
        - * **[Maintenance]:** Fixed out-of-order changelog entries.
        + * **[Release]:** Cut release v0.1.12 to finalize stability improvements.
        - * **[Release]:** Cut release v0.1.11 to finalize codebase stabilization.
        +  
        +  
        + ## [0.1.11] - 2026-05-20
        - ## [0.1.10] - 2026-04-16
        +  
        -  
        + ### Changed
        - ### Changed
        + * **[Assurance]:** Validated test suite fix for infinite loops caused by time.monotonic mocks and rich background threads. Ensured robust stateful mocking pattern is used.
        - * **[Assurance]:** Validated codebase structural integrity, ran adversarial QA, and ensured testing and static analysis fully pass. No regressions found after previous agent codebase maintenance.
        + * **[Maintenance]:** Fixed out-of-order changelog entries.
        - * **[Release]:** Cut release v0.1.10 to formalize the lifecycle assessment and finalize codebase stabilization.
        + * **[Release]:** Cut release v0.1.11 to finalize codebase stabilization.

   This is very messy because it shows multiple changes at once.

   Given the complexity and the fact that the git diff (head vs base) only shows a difference at the top and at the end (the newline), I suspect that the only difference between base and head is in the [0.1.14] section (the head has an extra Assurance bullet) and the missing newline at the end.

   But the context described many changes in the older versions.

   However, note the resolution rules: we must keep ALL meaningful changes from both branches.

   Since the git diff (head vs base) shows that the only difference between head and base is:
        - The addition of the Assurance bullet in the [0.1.14] section (and the rest of the file is the same, except for the newline at the end)

   then we should take the head branch's version for the [0.1