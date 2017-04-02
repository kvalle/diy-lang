# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.provision "shell", inline: <<-SCRIPT
    sudo apt-get install python-pip -y
    sudo pip install nose
SCRIPT

  config.vm.synced_folder "", "/home/vagrant/diy-lang"
end
