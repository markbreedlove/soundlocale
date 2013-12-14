
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


Known issues:
-------------
* The "allinone" configuration's provisioning isn't happening in the right
  order, such that the web application is started before the database is
  started, and returns an error, which stops the provisioning.  I'll fix this
  soon, but the "multiple" setup does work, if you want to use that.
* If you get errors about the vboxfs file system not being available, ssh into
  the virtual machine with "vagrant ssh <host>" and run "sudo
  /etc/init.d/vboxsf setup" and then restart the server (e.g. with "vagrant
  reload").  I'll eventually create an Ansible playbook to handle this
  situation, which is a known issue with Vagrant with regard to Debian's apt-get
  upgrade of kernel packages.

Tips:
-----
* If you want to switch between the "allinone" and "multiple" setups, you
  should destroy the existing VMs with "vagrant destroy" and then delete
  the .vagrant directory from this directory.  Then copy the desired
  Vagrantfile.<type> to Vagrantfile and do "vagrant up".
* You probably want to exclude $HOME/VirtualBox VMs/ from any backup jobs that
  you have going on, assuming you're just testing or developing.  The VMs can
  be recreated at any time, as long as you aren't storing data that you care
  about.

