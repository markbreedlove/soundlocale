
--== How to set up virtual machines with Vagrant and Ansible ==--

Install Vagrant, Virtualbox, and Ansible:
* Vagrant: http://www.vagrantup.com/downloads.html
* vagrant-vbguest: https://github.com/dotless-de/vagrant-vbguest/
* VirtualBox: https://www.virtualbox.org/wiki/Downloads
* Ansible: http://www.ansibleworks.com/docs/intro_installation.html
  (sudo pip install ansible)

Copy either Vagrantfile.allinone or Vagrantfile.multiple to Vagrant.  The
"allinone" file will create one virtual machine with the web, database, and
application, and "multiple" will create a separate VM for each.  Each one is
sized for 384 Mb of memory.  As a frame of reference, I find that I can
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

Reboot the server because kernel packages will probably have been updated:
$ vagrant reload

Make sure the app is running.  This is something I'll fix, but it doesn't start
on reboot.
$ vagrant ssh
vagrant@allinone:~$ sudo service soundlocale start

In your browser, go to:
http://vagrant.soundlocale.org/


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
* If you destroy and re-create a VM, you should delete the old public key
  from your $HOME/.ssh/known_hosts to avoid getting an error when you run
  "vagrant up" again.
