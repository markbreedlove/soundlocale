
Install Vagrant, Virtualbox, and Ansible:
* [vagrant url]
* [virtualbox url]
* [ansible url]

Copy either Vagrantfile.allinone or Vagrantfile.multiple to Vagrant.

Copy configuration_vagrant.py.dist to configuration_vagrant.py and edit the
mail-related settings.  For general demonstration / development use, you should
leave the other settings alone.

Add the following entry to your host name database (/etc/hosts on *nix
systems):
192.168.50.4    vagrant.soundlocale.org

Change into this directory in your shell:
$ cd /path/to/this/dir

Have Vagrant build and provision the servers:
$ vagrant up

In your browser, go to:
http://vagrant.soundlocale.org/

