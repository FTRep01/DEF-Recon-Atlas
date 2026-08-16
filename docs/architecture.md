# Architecture

```text
scope.json -> validator -> budget/rate limiter -> module -> evidence -> run.json -> report
```

All active modules receive a validated Scope. They cannot select arbitrary ports or paths outside the scope.
