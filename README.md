# sit747_repo
`sit746 experiments jupyter.ipynb` contains all the code that combines all scripts to run each experiment in Jupyter Notebook.  

`SingleStockKFohlcvCuilogr.py` contains the environment class script for running the main experiments with Cui et al (2023) as a baseline.  

`SingleStockohlcvCuilogr_no_kalman.py` contains the environment class script for running the ablation experiment with the removal of the Kalman Filter.  

In the case Yahoo Finance is down, I have uploaded all Excel files of all the OHCLV data used in this experiment.   

You can directly import the Excel files into Python using pandas. The thesis will dictate which versions of each package was used. 

To run the Jupyter notebook make sure the environment python scripts are in the same folder.

Research papers folder contains all literature papers. Task 2.1D is the draft literature review and task 2.2D is the research methodology. 

All experiments were conducted under Python 3.11, with exact package versions to ensure bit-wise
reproducibility of results. The key dependencies are:
NumPy 1.26.4
pandas 2.2.3
YahooFinance 0.2.58
PyTorch 2.0.0+cu126
PyKalman 0.10.1
Matplotlib 3.9.2


