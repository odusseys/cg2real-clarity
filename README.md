# Installation

```
pip install -r requirements.txt
```

You must also possess a Replicate API token, available at [Replicate.com](https://replicate.com/)

# Usage

## CLI

With `path_in` the path to the image to transform and `path_out` the path to write the result:

```
REPLICATE_API_TOKEN=<your token> python run.py <path_in> <path_out>
```

## Python

```
from cg2real import upscale

upscale(path_in, path_out)
```
