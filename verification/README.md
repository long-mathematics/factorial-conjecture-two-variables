# Verification records

Running

```sh
make test
```

writes exact-check records to this directory:

- `degree6.json` from `scripts/verify_degree6.py`;
- `identities.json` from `scripts/verify_identities.py`.

These files record finite symbolic and exact-arithmetic checks. They are reproducibility artifacts, not a formal verification of the universal FC(2) theorem, analytic continuation, polynomial monodromy, or the EIT I input.
