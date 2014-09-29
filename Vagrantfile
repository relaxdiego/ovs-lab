# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

# NOTE: Netmask is assumed 255.255.255.0 for all

SERVER1_TUNNEL_IP      = "192.168.1.10"
SERVER1_TUNNEL_GATEWAY = "192.168.1.254"
SERVER1_MGMT_IP        = "192.168.101.10"

SERVER2_TUNNEL_IP      = "192.168.2.20"
SERVER2_TUNNEL_GATEWAY = "192.168.2.254"
SERVER2_MGMT_IP        = "192.168.101.20"

INTERNET_MGMT_IP       = "192.168.101.254"


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"


  # "INTERNET"
  config.vm.define "internet" do |server|
    server.vm.hostname = "internet"

    # Server 1 tunnel transport network
    server.vm.network "private_network",
                      virtualbox__intnet: "server1_net",
                      ip: SERVER1_TUNNEL_GATEWAY,
                      netmask: "255.255.255.0"

    # Server 2 tunnel transport network
    server.vm.network "private_network",
                      virtualbox__intnet: "server2_net",
                      ip: SERVER2_TUNNEL_GATEWAY,
                      netmask: "255.255.255.0"

    # Management/Control network
    server.vm.network "private_network",
                      ip: INTERNET_MGMT_IP,
                      netmask: "255.255.255.0"

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

    # Tunnel transport network
    server.vm.network "private_network",
                      virtualbox__intnet: "server1_net",
                      ip: SERVER1_TUNNEL_IP,
                      netmask: "255.255.255.0"

    # Management/Control network
    server.vm.network "private_network",
                      ip: SERVER1_MGMT_IP,
                      netmask: "255.255.255.0"

    server.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--memory", 256]
      vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
    end

    # Not persistent across reboots!
    server.vm.provision "shell", inline: "route add #{SERVER2_TUNNEL_IP}/32 gw #{SERVER1_TUNNEL_GATEWAY} dev eth1"

    server.vm.provision "puppet" do |puppet|
      puppet.manifests_path = "puppet/manifests"
      puppet.manifest_file  = "site.pp"
      puppet.options = "--verbose --debug"
    end
  end


  # SERVER 2
  config.vm.define "server2" do |server|
    server.vm.hostname = "server2"

    # Tunnel transport network
    server.vm.network "private_network",
                      virtualbox__intnet: "server2_net",
                      ip: SERVER2_TUNNEL_IP,
                      netmask: "255.255.255.0"

    # Management/Control network
    server.vm.network "private_network",
                      ip: SERVER2_MGMT_IP,
                      netmask: "255.255.255.0"

    server.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--memory", 256]
      vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
    end

    # Not persistent across reboots!
    server.vm.provision "shell", inline: "route add #{SERVER1_TUNNEL_IP}/32 gw #{SERVER2_TUNNEL_GATEWAY} dev eth1"

    server.vm.provision "puppet" do |puppet|
      puppet.manifests_path = "puppet/manifests"
      puppet.manifest_file  = "site.pp"
      puppet.options = "--verbose --debug"
    end
  end


end
