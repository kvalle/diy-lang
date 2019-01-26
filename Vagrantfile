# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.provision "shell", inline: <<-SCRIPT
    sudo apt-get update
    sudo apt-get install python3 -y
    sudo apt-get install python3-pip -y
    sudo pip3 install nose
SCRIPT

  config.vm.synced_folder "", "/home/vagrant/diy-lang"
end
