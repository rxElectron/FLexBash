#!/bin/bash

# Start of sample script

echo "Script started"

cd /home/user/projects && ls -la > output.txt
if [ $USER == "root" ]; then
    echo "Welcome, root user"
else
    echo "Welcome, regular user"
fi

for file in *.txt; do
    cp "$file" /backup/
done

while true; do
    echo "Press Ctrl+C to stop"
    sleep 1
done

sudo pacman -Syu
chmod 755 script.sh
chown user:user script.sh
makepkg -si
tar -czvf archive.tar.gz /home/user/projects

echo "Script completed successfully"
exit 0