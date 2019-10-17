docker run -v D:\\Documents\Notebooks:/documents -i -t -p 8888:8888 -p 9000:9000 ntnu-lectures /bin/bash --login -c "/opt/conda/bin/conda install jupyter -y --quiet && /opt/conda/bin/jupyter notebook --notebook-dir=/documents --ip='*' --port=8888 --no-browser --allow-root"

