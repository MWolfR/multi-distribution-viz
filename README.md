# multi-distribution-viz
For visualizations of the distribution of data with values for multiple categories

by Michael W. Reimann

This tool generates an interactive visualization of the distribution of data points that have labels
in various categories assigned to it. That is, each data point is associated with those labels.
The labels can be for example names of organisms or age groups. The data must be formatted as follows:
1. It must be a pandas.Series that has been exported using .to_pickle(..., protocol=4)
2. The Series must use a MultiIndex with named columns
3. Each value of the Series must be list of numerical values
4. This list holds all values associated with that combination of labels.
5. Not every combination of labels needs to have data associated with it.

As an example let's take some samples of weight (in grams) of organisms:

    Species       Age     Sex
    mouse         young   male    [4.0, 5.5, 4.3, 3.4]
                          female  [3.5, 6.5, 7.0, 5.5]
                  old     male    [10.5, 15.4]
                          female  [12.2, 19.0, 18.1]
    dog           old     male    [4010.0, 3250.0]
                          female  [3590.0]
                  old     female  [22510.0, 32100.0]
    elephant      young   male    [125000.0, 165000.0, 180000.0]
                  old     female  [4512000.0]
    dtype: float64

A more complex example, a visualization of topological parameters associated with neurons in various
regions of the SSCX model of the BBP is deployed under:

https://topo-characterization.herokuapp.com/

**Getting started**

To start with, let's generate the distribution of topological parameters mentioned above. The data for this is already part of the repository.

1. Clone the repository from github:

    `git clone https://github.com/MWolfR/multi-distribution-viz`
    
    `cd multi-distribution-viz`

2. Ensure that your python version matches the specified runtime:

    `cat runtime.txt`

    `python-3.7.3`

    It will probably work in any python-3 version. But only the specified version is officially supported.

3. Install requirements

    `pip install -r requirements.txt`

4. (Optional) install gunicorn
This step is not required, but you can apt-get install gunicorn and then pip install gunicorn

5. Run the example. Simply point the main script at the data payload, formatted as above

    `python viz_distribution_index.py data/contracted_db.pkl`

    `Serving Flask app "viz_multi_index" (lazy loading)
    Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    Debug mode: off
    Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)`


If you have installed gunicorn you can alternatively run:

    gunicorn 'viz_distribution_index:main(["data/contracted_db.pkl"])'


    [2020-04-22 09:53:33 +0200] [10516] [INFO] Starting gunicorn 20.0.4
    [2020-04-22 09:53:33 +0200] [10516] [INFO] Listening at: http://127.0.0.1:8000 (10516)
    [2020-04-22 09:53:33 +0200] [10516] [INFO] Using worker: sync
    [2020-04-22 09:53:33 +0200] [10519] [INFO] Booting worker with pid: 10519


Finally, just navigate your browser to the specified url

You can also do it with your own payload data, as long as it satisfies the prerequisites listed above.
The GUI is optimized for data that has four categories. If there's more than that, the GUI might get cramped.
Note that you can also load several payload files at once.

    `python viz_distribution_index.py data/file1.pkl data/file2.pkl data/file3.pkl`

In that case, the data in the individual files will be concatenated.
