docker run -v D:\\Documents\Notebooks:/documents -i -t -p 8889:8889 -p 8888:8888 ntnu-lectures /bin/bash --login -c "/opt/conda/bin/conda install jupyterlab -y --quiet && /opt/conda/bin/jupyter lab --notebook-dir=/documents --ip='*' --port=8888 --no-browser --allow-root"

