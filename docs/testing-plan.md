# Testing Plan

## Backend tests

- Health endpoint returns 200
- Summary endpoint returns expected keys
- Technology adoption endpoint returns list
- Regional usage endpoint returns list
- Usage event limit parameter works

## Frontend checks

- Dashboard loads when backend is running
- Error message appears when backend is not running
- Summary metric cards display data
- Charts render with API data

## Future improvements

- Add create/update/delete endpoint tests
- Add Playwright end-to-end test
- Add frontend unit tests
- Add database validation tests
