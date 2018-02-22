Vagrant.configure(2) do |config|
  config.vm.define 'request_attacker'
  config.vm.box = 'ubuntu/xenial64'
  config.vm.provider :virtualbox do |v|
    v.cpus   = 2
    v.memory = 2048
  end

  config.vm.network :forwarded_port, host: 8080, guest: 8080
  #config.vm.provision "file", source: "/Users/kazu/workspace/requests_attacker", destination: "$HOME/"
  config.vm.provision 'shell', inline: <<-EOS
    sudo apt-get update
    sudo apt-get upgrade -y
    sudo apt-get install -y python3-pip python3-dev
    sudo -H pip3 install -r $HOME/request_attacker/requirements.txt
  EOS
end
