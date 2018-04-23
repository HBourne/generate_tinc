#!/bin/sh
sendlist="./sendlist"
repo="./tinc-key"
# NODENAME=
# CONNECTTO=
# NODEIP=
# VPNIP=


# Get the newest version of repo of keys
git clone ssh://git@git.infervision.com:2222/diffusion/64/tinc-key.git

# Check whether the NODEIP already exists
grep $NODEIP $repo/nodelist && exit 999

# mkdir if the paths don't exist
if [ ! -x $sendlist ]; then
	mkdir $sendlist
fi

mkdir -p tx/hosts

# Generate tinc.conf and copy server configuration files
echo "Name = $NODENAME
AddressFamily = ipv4
Mode = Switch" > tx/tinc.conf

if [ $CONNECTTO ]; then
	IFS=','
	for cnct in $CONNECTTO
	do
		echo "ConnectTo = $cnct" >> tx/tinc.conf
		cp $repo/$cnct/$cnct tx/hosts || exit 100
	done
fi

# Generate tinc-up
echo "#!/bin/bash
ifconfig \$INTERFACE $NODEIP netmask 255.255.255.0" >> tx/tinc-up

# Generate tinc-down
echo "#!/bin/bash
ifconfig \$INTERFACE down" >> tx/tinc-down

# Chmod of tinc-*
chmod 775 tx/tinc-*

# Generate hosts config
if [ $VPNIP ]; then
	IFS=','
	for vpnip in $VPNIP
	do
		echo "Address = $vpnip" >> tx/hosts/$NODENAME
	done
else
	touch tx/hosts/$NODENAME || exit 111
fi

# Generate and save pub & priv key
if [ -d "$repo/$NODENAME" ]; then
	cp $repo/$NODENAME/$NODENAME tx/hosts/ || exit 200
	cp $repo/$NODENAME/rsa_key.priv tx/ || exit 300
else
	"\r" | tincd -c tx -n tx -K4096
	mkdir -p $repo/$NODENAME
	find tx/rsa_key.pub && (cp tx/rsa_key.pub tx/hosts/$NODENAME || exit 546)
	cp tx/hosts/$NODENAME $repo/$NODENAME/ || exit 400
	cp tx/rsa_key.priv $repo/$NODENAME/ || exit 500
fi

# Generate tar file
tar czf $sendlist/"$NODENAME".tar tx/

# Remove tincconf file
rm -r tx

# Update the repo
echo "$NODENAME $NODEIP" >> $repo/nodelist
cd $repo && git add . && git commit -m "$NODENAME added" && git push && cd ..
