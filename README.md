feynapps_panel
==============

OpenStack Horizon Panel for image contextualization

## Get the package 

Install the package using pip:
```
pip install git+https:/github.com/IFCA/feynapps_panel.git@stable/grizzly#egg=feynapps_panel
```

Or by cloning and using the setup.py provided:
```
git clone -b stable/grizzly https://github.com/IFCA/feynapps_panel.git ; cd feynapps_panel; python setup.py install
```

## Add to INSTALLED_APPS

Add `'feynapps_panel'` to the `INSTALLED_APPS` of your django settings.

You can add it in the global `settings.py` file (In ubuntu it's
located at `/usr/share/openstack-dashboard/openstack_dashboard/settings.py`)

Or in your `local_settings.py` with the following lines:
```
import sys
mod = sys.modules['openstack_dashboard.settings']
mod.INSTALLED_APPS += ('feynapps_panel',)
```

Then restart apache:
```
service apache2 restart
```

## Extra Configuration

In your `local_settings.py` file you can also configure the following variables:

* `FEYNAPPS_URL`: URL for the apps.json file with the application description,
  default value: `'https://raw.github.com/enolfc/feynapps/master/apps.json'`

* `FEYNAPPS_REPO`: (not used currently) URL of the git repo, default value `'http://github.com/enolfc/feynapps.git'`, 

* `FEYNAPPS_IMG_ATTR`: property of the images enabled to use the contextualizer (default: `feynapps`)

