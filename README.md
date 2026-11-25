# Indexability Triage Lab

A small interactive educational tool for understanding hypothetical Google Search technical signals. Ten fictional cases and adjustable observations make it possible to compare a starting case with a changed one. No URLs are collected, no external API or crawling requests are made, no accounts or tokens are required by the app, and no custom analytics or persistent storage are included.

The deterministic rules are an intentionally simplified triage workflow, not a reproduction of Google's indexing algorithm or proof of actual indexability. They preserve the distinction between blocked crawling and observed noindex, canonical hints and Google-selected canonicals, and temporary errors and missing information. See the official documentation linked in the app.

## Run locally

```sh
python -m pip install -r requirements.txt
streamlit run app.py
```

## Test the rule engine

```sh
python -m unittest -v test_triage
```

The reference cases, targeted regressions, and every combination of the UI's 12 status, 3 crawl, 3 directive, 3 canonical, and 3 content settings are checked. Native Streamlit runtime testing is separate from rule-engine tests.

Original AI-assisted educational example from [DigestSEO](https://digestseo.com/) and [engineering portfolio](https://tomiseregi.si/). Not affiliated with Google. No production data or proprietary code.
