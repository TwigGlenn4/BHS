name: Update README.md

on:
  schedule:
    - cron: '0 * * * *' # Run every hour

jobs:
  update_readme:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Update README.md
      run: |
        python3 update_readme.py
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add README.md
        git commit -m "Update server status in README.md"
        git push
