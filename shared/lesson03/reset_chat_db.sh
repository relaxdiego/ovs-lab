ovs-appctl -t ovsdb-server exit

if [ ! -d "/etc/lesson03" ]; then
  mkdir /etc/lesson03
else
  rm -f /etc/lesson03/chat.db
fi

ovsdb-tool create /etc/lesson03/chat.db /vagrant/shared/lesson03/chat.ovsschema
ovsdb-server --pidfile --detach --log-file --remote punix:/var/run/openvswitch/db.sock /etc/lesson03/chat.db
ovs-appctl -t ovsdb-server ovsdb-server/add-remote ptcp:6640
ovs-appctl -t ovsdb-server vlog/set dbg
