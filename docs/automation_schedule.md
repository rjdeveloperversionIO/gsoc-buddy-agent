# GSoC Buddy Automation Schedule

This document outlines the automation schedule for the GSoC Buddy agent, including regular schedules, event-based triggers, and workflow dependencies.

## Regular Scheduled Tasks

| Task | Schedule | Frequency | Timing Rationale | Resource Usage |
|------|----------|-----------|------------------|----------------|
| Issue Scanner | `0 */6 * * *` | Every 6 hours | Balances freshness with API limits | ~500 GitHub API calls/run |
| Issue Status Updater | `0 */12 * * *` | Every 12 hours | Less urgent than new issue discovery | ~200 GitHub API calls/run |
| Organization Enrichment | `0 0 * * 0` | Weekly (Sunday) | Organization data changes infrequently | ~100 GitHub API calls/run |
| Student-Issue Matcher | `0 */8 * * *` | Every 8 hours | Follows issue scanner with buffer for analysis | Minimal API usage |
| Daily Digest Generator | `0 17 * * *` | Daily at 5 PM UTC | End of day for most time zones | Minimal API usage |
| Weekly Summary | `0 15 * * 5` | Weekly (Friday) | End of week recap | Minimal API usage |
| Database Cleanup | `0 2 * * 0` | Weekly (Sunday) | Low-traffic period | Moderate database usage |
| Health Check | `0 */4 * * *` | Every 4 hours | Regular system verification | Minimal API usage |

## Event-Based Triggers

| Event | Trigger Source | Actions Triggered | Delay | Throttling |
|-------|---------------|-------------------|-------|------------|
| New Issue Created | GitHub Webhook | Issue Analysis, Matching | None | Max 10/minute |
| Issue Status Changed | GitHub Webhook | Update Issue Status, Notify Students | None | Max 20/minute |
| New Student Registration | Telegram/Discord Bot | Profile Creation, Initial Matching | None | No limit |
| Student Profile Updated | Bot Command | Update Profile, Re-run Matching | 5 minutes | Max 5/minute |
| Match Feedback Received | Bot Interaction | Update Match Quality, Adjust Algorithm | None | No limit |
| GSoC Timeline Event | Calendar API | Update Phase, Adjust Weights | None | No limit |

## Workflow Dependencies

```ascii
┌─────────────────┐
│  Issue Scanner  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ Issue Analyzer  │────►│ Student-Issue   │
└─────────────────┘     │    Matcher      │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  Notification   │
                        │   Dispatcher    │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Student         │
                        │ Interaction     │
                        └─────────────────┘
```
# Resource Optimization Strategies

## API Rate Limit Management
- Track remaining rate limits in each API response
- Implement exponential backoff for retries
- Distribute API-intensive tasks throughout the day
- Cache responses where appropriate

## Batch Processing
- Group similar API calls together
- Process issues in batches of 50
- Bulk update database records
- Combine notifications when possible

## Incremental Updates
- Only scan repositories with recent activity
- Only update changed issue statuses
- Prioritize active students and organizations

## Parallel Processing
- Run independent workflows in parallel
- Split large scans into multiple smaller jobs
- Use concurrent API requests where supported

# Manual Override Triggers

All automated workflows can also be triggered manually through:
- GitHub Actions UI (Run workflow button)
- Bot commands (e.g., `/scan`, `/match`, `/digest`)
- Admin dashboard

# Monitoring and Alerts

- Failed workflow runs trigger email notifications
- Rate limit warnings sent to admin Telegram chat
- Daily health report summarizes all workflow executions
- Error logs stored in dedicated worksheet

# GSoC Phase-Specific Adjustments

| Phase | Date Range | Scanner Frequency | Matcher Frequency | Notification Strategy |
|-------|------------|-------------------|-------------------|------------------------|
| Pre-announcement | Before Feb | 12 hours | 24 hours | Weekly digest only |
| Organization Announcement | Feb-Mar | 6 hours | 12 hours | Daily digest + high priority |
| Student Application | Mar-Apr | 6 hours | 8 hours | Daily digest + all matches |
| Project Acceptance | May | 6 hours | 8 hours | Daily digest + high priority |
| Coding Period | Jun-Aug | 6 hours | 12 hours | Daily digest + high priority |
| Wrap-up | Sep | 12 hours | 24 hours | Weekly digest only |
