$BinDir = "P:\dev\python-dev\tchou-server\dist"
ssh ubuntu@192.168.1.30 "rm /home/ubuntu/tchou/tchou-server/pkg/tchou*.whl"
scp $BinDir\tchou*.whl ubuntu@192.168.1.30:/home/ubuntu/tchou/tchou-server/pkg
Start-Sleep -Seconds 5