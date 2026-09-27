---
name: task-lanes
description: Classify AI-assisted work into a small interactive lane or an asynchronous lane before execution. Use when work is competing for attention or needs an agent handoff.
---

# Task lanes

Choose the lane that protects the user's attention while still meeting the task's deadline.

Use the **interactive lane** for a small, bounded action whose result changes the next decision: a targeted edit, a question about a file, a short diagnosis, or a quick experiment. Keep at most two or three active interactive tasks. Return a concise result or a concrete decision point promptly.

Use the **asynchronous lane** for work with a clear deliverable but no need for continuous steering: repository exploration, long diagnostics, multi-file changes, research synthesis, or a build-and-fix cycle. State the expected output, completion checks, and stopping conditions before starting. Work independently and report a compact handoff when finished.

If the task is ambiguous, first reduce it to a brief task contract. Do not create parallel work merely because parallelism is available; use it only when the outputs are independent and the user can reasonably review them.
