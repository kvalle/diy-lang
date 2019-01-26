# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"

  config.vm.provision "shell", inline: <<-SCRIPT
    sudo apt-get install python-pip -y
    sudo apt-get install python-nose
SCRIPT

  config.vm.synced_folder "", "/home/vagrant/diy-lang"
end
