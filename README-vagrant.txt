
--== How to set up virtual machines with Vagrant and Ansible ==--

Install Vagrant, Virtualbox, and Ansible:
* http://www.vagrantup.com/downloads.html
* https://www.virtualbox.org/wiki/Downloads
* http://www.ansibleworks.com/docs/intro_installation.html
  (sudo pip install ansible)

Copy either Vagrantfile.allinone or Vagrantfile.multiple to Vagrant.

Copy configuration_vagrant.py.dist to configuration_vagrant.py and edit the
mail-related settings.  For general demonstration / development use, you should
leave the other settings alone.

Add the following entry to your host name database (/etc/hosts on *nix
systems):
192.168.50.4    vagrant.soundlocale.org

In your shell, change into the directory that contains this file:
$ cd /path/to/this/dir

Have Vagrant build and provision the servers:
$ vagrant up

In your browser, go to:
http://vagrant.soundlocale.org/

If you run into any issues with this installation, please let me know!

