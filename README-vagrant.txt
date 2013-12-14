
--== How to set up virtual machines with Vagrant and Ansible ==--

Install Vagrant, Virtualbox, and Ansible:
* http://www.vagrantup.com/downloads.html
* https://www.virtualbox.org/wiki/Downloads
* http://www.ansibleworks.com/docs/intro_installation.html
  (sudo pip install ansible)

Copy either Vagrantfile.allinone or Vagrantfile.multiple to Vagrant.  The
"allinone" file will create one virtual machine with the web, database, and
application, and "multiple" will create a separate VM for each.  Each one takes
up about 400 to 420 MB of memory.  As a frame of reference, I find that I can
run all three easily enough on Mac OS X 10.9, with 4 GB memory, while running a
web browser and a number of shell sessions.

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

