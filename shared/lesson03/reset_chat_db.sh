ovs-appctl -t ovsdb-server exit

if [ ! -d "/etc/chatdb" ]; then
  mkdir /etc/chatdb
else
  rm /etc/chatdb/chat.db
fi

ovsdb-tool create /etc/chatdb/chat.db /vagrant/shared/lesson03/chat.ovsschema
ovsdb-server --pidfile --detach --log-file --remote punix:/var/run/openvswitch/db.sock /etc/chatdb/chat.db
ovs-appctl -t ovsdb-server ovsdb-server/add-remote ptcp:6640
ovs-appctl -t ovsdb-server vlog/set dbg
