# Install ML Deps

## Problem:
Encountered dependency missing error 
```shell
module not found- statsmodel
```
## Solution:

1. `poetry add --group ml statsmodels`
2. `poetry run streamlit run app.py`

And test the changes...