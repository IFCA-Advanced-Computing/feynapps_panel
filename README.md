feynapps_panel
==============

OpenStack Horizon Panel for image contextualization

## Installation

## Configuration

In your `settings.py` file you can configure the following variables:

* `FEYNAPPS_URL`: URL for the apps.json file with the application description,
  default value: `'https://raw.github.com/enolfc/feynapps/master/apps.json'`

* `FEYNAPPS_REPO`: (not used currently) URL of the git repo, default value `'http://github.com/enolfc/feynapps.git'`, 

* `FEYNAPPS_IMG_ATTR`: property of the images enabled to use the contextualizer (default: `feynapps`)

