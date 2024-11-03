## Available Backups

- backup_project_uncleed_site_ver_0.1.0
- backup_project_uncleed_site_ver_0.1.1


## Version History

| Version   | Description                        |
|-----------|------------------------------------|
| ver_0.1.0 | Full - Initial base release        |
| ver_0.1.1 | Headless - review system           |


## Task Breakdown for Mock Test Features

1. **Top 5 Mock Tests by Default**
   - [x] Implement logic to fetch and display the highest-ranked five mock tests based on:
     - [x] Average rating across the 7 characteristics.
     - [x] Default sorting criteria (e.g., most recent or highest clarity).
   - [ ] Create a UI component to display these mock tests.

2. **Customizable Sorting**
   - [x] Implement sorting functionality to allow users to reorder mock tests based on specific characteristics (e.g., clarity, difficulty).
   - [ ] Update the UI to include sorting options (e.g., dropdown menu).

3. **Flexible Comparison Feature**
   - **Selection Controls:**
     - [ ] Create a selection mechanism for users to choose multiple mock tests:
       - [ ] Limit selection for radar charts to 2 tests.
       - [ ] Limit selection for bar/line charts to 4 tests.
   - **User Interaction:**
     - [ ] Implement buttons or dropdowns to switch between chart types (radar, bar, line).
     - [ ] Allow users to dynamically add or remove mock tests from comparison.

4. **Chart Types with Toggle Option**
   - **Radar Chart:**
     - [ ] Implement radar chart to visualize scores across all 7 characteristics for 2 mock tests.
   - **Bar/Line Chart:**
     - [ ] Create bar/line charts to display characteristics side by side for up to 4 mock tests.
   - **Pie Chart (Optional):**
     - [ ] Implement a pie chart to show the distribution of scores for a single test's 7 characteristics.

5. **UI and Tooltips**
   - [ ] Design and implement tooltips or hover effects on each chart point to display additional information (e.g., precise scores).
   - [ ] Ensure tooltips enhance readability without crowding the main chart area.

### Additional Considerations
- [ ] Write unit tests for each functionality implemented.
- [ ] Document the usage of each feature in the README.
- [ ] Provide examples or screenshots of the charts in the README.
