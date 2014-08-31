node basenode {

  exec { "apt_get_update":
    command => "/usr/bin/apt-get -y update"
  }

  # Ensure the above command runs before we attempt
  # to install any package in other manifests
  Exec["apt_get_update"] -> Package<| |>

  package { "unzip":
    ensure => installed,
  }

  exec { "download_ovs":
    command => "/usr/bin/wget https://www.dropbox.com/sh/k5t492id6hc6ynf/AAA2GzeOowsf7Kdjv6eC5Yfca?dl=1 -O /vagrant/shared/ovs.zip",
    cwd     => "/root",
    creates => "/vagrant/shared/ovs.zip",
  }

  exec { "extract_ovs":
    command => "/usr/bin/unzip /vagrant/shared/ovs.zip -d /vagrant/shared/ovs",
    cwd     => "/vagrant/shared",
    require => [
                  Package["unzip"],
                  Exec["download_ovs"],
               ],
    returns => [0, 2],
    creates => "/vagrant/shared/ovs/openvswitch-common_2.3.0-1_amd64.deb",
  }

  package { "ovs_common":
    name     =>  "openvswitch-common",
    ensure   =>  installed,
    provider =>  dpkg,
    source   =>  "/vagrant/shared/ovs/openvswitch-common_2.3.0-1_amd64.deb",
    require  => [
                   Exec["extract_ovs"],
                ]
  }

  package { "ovs_switch":
    name     =>  "openvswitch-switch",
    ensure   =>  installed,
    provider =>  dpkg,
    source   =>  "/vagrant/shared/ovs/openvswitch-switch_2.3.0-1_amd64.deb",
    require  => [
                  Package["ovs_common"],
                ],
  }

}



node servernode inherits basenode {

  package { "ovs_python":
    name     =>  "python-openvswitch",
    ensure   =>  installed,
    provider =>  dpkg,
    source   =>  "/vagrant/shared/ovs/python-openvswitch_2.3.0-1_all.deb",
    require  => [
                  Package["ovs_common"],
                ],
  }

  package { "ovs_vtep":
    name     =>  "openvswitch-vtep",
    ensure   =>  installed,
    provider =>  dpkg,
    source   =>  "/vagrant/shared/ovs/openvswitch-vtep_2.3.0-1_amd64.deb",
    require  => [
                  Package["ovs_python"],
                ],
  }

  package { "mininet":
    ensure => installed,
    require => [
                  Package["ovs_switch"],
               ]
  }

}



import 'nodes/*.pp'
