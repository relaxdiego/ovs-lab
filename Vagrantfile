# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

# NOTE: Netmask is assumed 255.255.255.0 for both

SERVER1_IP      = "192.168.1.10"
SERVER1_GATEWAY = "192.168.1.254"

SERVER2_IP      = "192.168.2.20"
SERVER2_GATEWAY = "192.168.2.254"


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"


  # "INTERNET"
  config.vm.define "internet" do |server|
    server.vm.hostname = "internet"

    server.vm.network "private_network",
                     ip: SERVER1_GATEWAY,
                     netmask: "255.255.255.0",
                     virtualbox__intnet: "server1_net"

    server.vm.network "private_network",
                     ip: SERVER2_GATEWAY,
                     netmask: "255.255.255.0",
                     virtualbox__intnet: "server2_net"

    server.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--memory", 256]
      vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
    end

    # Not persistent across reboots!
    server.vm.provision "shell", inline: "echo 1 > /proc/sys/net/ipv4/ip_forward"

    server.vm.provision "puppet" do |puppet|
      puppet.manifests_path = "puppet/manifests"
      puppet.manifest_file  = "site.pp"
      puppet.options = "--verbose --debug"
    end
  end


  # SERVER 1
  config.vm.define "server1" do |server|
    server.vm.hostname = "server1"

    server.vm.network "private_network",
                     ip: SERVER1_IP,
                     netmask: "255.255.255.0",
                     virtualbox__intnet: "server1_net"

    server.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--memory", 256]
      vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
    end

    # Not persistent across reboots!
    subnet = "#{SERVER2_IP.split('.').take(3).join('.')}.0"
    server.vm.provision "shell", inline: "route add -net #{subnet}/24 gw #{SERVER1_GATEWAY} dev eth1"

    server.vm.provision "puppet" do |puppet|
      puppet.manifests_path = "puppet/manifests"
      puppet.manifest_file  = "site.pp"
      puppet.options = "--verbose --debug"
    end
  end


  # SERVER 2
  config.vm.define "server2" do |server|
    server.vm.hostname = "server2"

    server.vm.network "private_network",
                     ip: SERVER2_IP,
                     netmask: "255.255.255.0",
                     virtualbox__intnet: "server2_net"

    server.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--memory", 256]
      vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
    end

    # Not persistent across reboots!
    subnet = "#{SERVER1_IP.split('.').take(3).join('.')}.0"
    server.vm.provision "shell", inline: "route add -net #{subnet}/24 gw #{SERVER2_GATEWAY} dev eth1"

    server.vm.provision "puppet" do |puppet|
      puppet.manifests_path = "puppet/manifests"
      puppet.manifest_file  = "site.pp"
      puppet.options = "--verbose --debug"
    end
  end


end
