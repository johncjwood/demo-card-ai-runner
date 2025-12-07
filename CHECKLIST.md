# Checklist

- [x] Ask top 3 clarifying questions
- [x] Review current test execution logic
- [x] Fix the logic to skip higher C values when a lower C succeeds
- [ ] Verify the fix works correctly

## Original User Prompt

I see this output:
unning R0/L1/C1...
Completed R0/L1/C1 - PASS
Running R0/L1/C2...
Completed R0/L1/C2 - PASS
Running R0/L1/C3...

However, the logic should be that if a lower L or C succeeds, then the later ones should be skipped. In this case, R0/L1/C1 succeeded, so R0/L1/C2 should not have run since C2 is higher than C1
