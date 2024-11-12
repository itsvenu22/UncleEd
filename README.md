## Available Backups

- backup_project_uncleed_site_ver_0.1.0
- backup_project_uncleed_site_ver_0.1.1
- backup_project_uncleed_site_ver_0.1.2

## Version History

| Version   | Description                          |
|-----------|--------------------------------------|
| ver_0.1.0 | Full - Initial base release          |
| ver_0.1.1 | Headless - review system             |
| ver_0.1.2 | Full - Analytics and Mock Comparison |





When you merge your dev branch into the main branch, the contribution heatmap will show the day of the merge as a single commit, unless you perform a squash merge or rebase beforehand.

Here's the breakdown:

Regular Merge:

The contribution heatmap will only reflect the day you merged the dev branch into the main branch.
The individual daily commits on the dev branch won't be shown on the heatmap. Instead, it will show a single commit on the day of the merge.
Squash Merge:

If you squash your commits before merging (e.g., using git merge --squash), all the changes from the dev branch will be squashed into a single commit.
The heatmap will only show one commit on the day of the squash merge.
Rebase:

If you rebase your dev branch onto the main branch, each individual commit on the dev branch will be preserved and can reflect the dates of those commits on the heatmap.
After rebasing, if you merge or push the changes, the commits on the dev branch will appear as if they were made directly on main, and the heatmap will show the individual commit dates.
To summarize, if you simply merge without squashing or rebasing, only the merge commit day will show up on the heatmap. If you want all your individual daily commits to show, you would need to rebase or push them as individual commits to the main branch.
