broday_ip="10.0.88.173"
ben_ip="10.0.89.7"

broday_ports=""
ben_ports=""

if [ $1 ] && [ $2 ]
then
	ports=$(seq $1 $2)
else
	echo "Pass a range of ports as arguments"
	exit
fi

for port in ${ports}
do
	broday_ports="${broday_ports}${broday_ip}:${port} "
	ben_ports="${ben_ports}${ben_ip}:${port} "
done

echo ${broday_ports}
echo ${ben_ports}

redis-cli --cluster create ${broday_ports}${ben_ports}--cluster-replicas 1
