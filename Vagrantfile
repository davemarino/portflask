# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise32"

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine.
  config.vm.network :forwarded_port, guest: 8000, host: 8000
  # Give the vagrant guest an IP accessible only from the host
  config.vm.network :private_network, ip: "192.168.111.223"

  # Provision the guest with a shell script
  config.vm.provision :shell, :path => "vagrantbootstrap.sh"

  # Pass SSH keys through to the VM so git will work normally
  config.ssh.forward_agent = true

end
