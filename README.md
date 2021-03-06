[![DOI](https://zenodo.org/badge/235116234.svg)](https://zenodo.org/badge/latestdoi/235116234)

This contains all the necessary resources to generate the figures in the article

Manik, D., Molkenthin, N. *Topology dependence of on-demand ride-sharing*. **Appl Netw Sci** 5, 49 (2020). https://doi.org/10.1007/s41109-020-00290-2, 
https://arxiv.org/abs/2001.09711.  


HOWTO
-----

1. Install the software

```bash
# Create a new virtualenv and activate it
python3.6 -m venv venv
source venv/bin/activate
# install depndencies
pip install -r requirements.txt
pip install -e ./
```

2. Download streetnetworks using OSMnx for figures 5-6. Execute `generate_data_and_plot/gen_streetnetworks_for_simulations.ipynb`.

3. Run the simulations. This can be done by running `generate_data_and_plot/generate_all_data.py`. This is a time and resource
intensive step, which is best done parallely in an HPC cluster. Ways to do so are described in `generate_data_and_plot/cluster_generate_all_data.py`

4. Now the figures can be generated. Execute the notebooks `generate_data_and_plot/fig_.*.ipynb`.
