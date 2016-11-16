# -*- coding: utf-8 -*-

version = '4.3.12'

from setuptools import setup, find_packages

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='cpskin.policy',
      version=version,
      description='Policy package for cpskin',
      long_description=long_description,
      classifiers=[
          "Environment :: Web Environment",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
      ],
      keywords='',
      author='IMIO',
      author_email='support@imio.be',
      url='https://github.com/imio/cpskin.policy',
      license='gpl',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'collective.contentrules.runscript',
          'collective.geotransform',
          'cpskin.agenda',
          'cpskin.caching',
          'cpskin.core',
          'cpskin.diazotheme.classic',
          'cpskin.menu',
          'cpskin.minisite',
          'cpskin.slider',
          'cpskin.theme',
          'cpskin.workflow',
          'collective.directory',
          'Products.PasswordStrength',
          'collective.jekyll',
          'Products.PloneFormGen',
          'Products.PloneGazette',
          'Solgema.fullcalendar',
          'collective.atomrss',
          'collective.monitor',
          'collective.cookiecuttr',
          'plone.app.imagecropping',
          'imio.migrator',
          'collective.excelexport',
          'collective.autoscaling',
          'collective.preventactions',
          'collective.recaptcha',
      ],
      extras_require=dict(
          test=['plone.app.robotframework', 'cpskin.demo']
      ),
      entry_points={})
