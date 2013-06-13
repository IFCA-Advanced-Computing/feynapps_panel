# coding=utf-8

# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
# Copyright (c) 2012, Spanish National Research Council
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from setuptools import setup


setup(
    name='feynapps_panel',
    version='1.0',
    description='FeynApps panel for Horizon (stable/grizzly).',
    long_description='''OpenStack Horizon panel for image contextualization
with various Phenomenology applications (FeynHiggs, FeynArts, LoopTools, etc).
''',
    classifiers=[
        'Programming Language :: Python'
        'Development Status :: 5 - Production/Stable',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords='',
    author='Spanish National Research Council',
    author_email='enolfc@ifca.unican.es',
    url='http://www.ifca.es',
    license='Apache License, Version 2.0',
    include_package_data=True,
    packages=['feynapps_panel'],
    package_data={
        'feynapps_panel': ['templates/feynapps_panel/*.html']
    },
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
)
