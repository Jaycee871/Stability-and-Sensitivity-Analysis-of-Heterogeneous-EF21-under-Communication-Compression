# Hugging Face connection

The repository can optionally use the repository secret `HF_TOKEN1` for authenticated Hugging Face API checks from GitHub Actions.

The CI connectivity step sends the token only in the HTTP `Authorization` header to `https://huggingface.co/api/whoami-v2`, checks for HTTP 200, and does not print the token or response body.

This is an authentication smoke test only. It does not publish, modify, or delete Hugging Face resources.
