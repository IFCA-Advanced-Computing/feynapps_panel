feynapps_panel
==============

OpenStack Horizon Panel for image contextualization

## Installation

Get the code and install the python package:

```
$ git clone  https://github.com/IFCA/feynapps_panel.git
$ cd feynapps_panel
$ sudo python setup.py install
```

Add `'feynapps_panel'` to the `INSTALLED_APPS` of the `settings.py` file (In ubuntu it's
located at `/usr/share/openstack-dashboard/openstack_dashboard/settings.py`)

And restart apache:
```
$ sudo service apache2 restart
```

## Configuration

In your `local_settings.py` file you can also configure the following variables:

* `FEYNAPPS_URL`: URL for the apps.json file with the application description,
  default value: `'https://raw.github.com/enolfc/feynapps/master/apps.json'`

* `FEYNAPPS_REPO`: (not used currently) URL of the git repo, default value `'http://github.com/enolfc/feynapps.git'`, 

* `FEYNAPPS_IMG_ATTR`: property of the images enabled to use the contextualizer (default: `feynapps`)

