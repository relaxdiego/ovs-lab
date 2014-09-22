ovs-appctl -t ovsdb-server exit
rm /etc/tododb/todo.db
ovsdb-tool create /etc/tododb/todo.db /vagrant/shared/lesson03/todo.ovsschema
ovsdb-server --pidfile --detach --log-file --remote punix:/var/run/openvswitch/db.sock /etc/tododb/todo.db
ovs-appctl -t ovsdb-server ovsdb-server/add-remote ptcp:6640
