name: PR Labeler

on:
  pull_request_target:
    types: [opened, synchronize]

jobs:
  label:
    permissions:
      contents: read
      pull-requests: write
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v4
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          configuration-path: .github/labeler.yml

      - name: Label first-time contributors
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          chmod +x .github/scripts/first-time-contributor.sh
          ./.github/scripts/first-time-contributor.sh \
            "${{ github.event.pull_request.user.login }}" \
            "${{ github.event.pull_request.number }}" \
            "${{ github.repository }}" \
            "${{ secrets.GITHUB_TOKEN }}"