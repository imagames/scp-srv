# scp-srv

This script resolves wraps SCP and uses SRV records to resolve hosts and ports.

To use: 

```bash
pip3 install -r requirements.txt
./scp-srv.py [normal scp arguments]
```

When inputting a host with SRV records, don't add the `_ssh._tcp.` part. The script will take care of that.

It's recommended to symlink this script somewhere in your `PATH`.
