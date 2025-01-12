#!/usr/bin/env bash

# Function to display a progress bar
progress_bar() {
    local PROG_BAR='####################'
    local BLANK_BAR='                    '
    local PROGRESS=$1
    printf "\r[%.*s%.*s] %d%%" $PROGRESS "$PROG_BAR" $((20-PROGRESS)) "$BLANK_BAR" $((PROGRESS*5))
}

# Check if patchelf is installed, if not, install it
if ! command -v patchelf &> /dev/null
then
    echo "patchelf could not be found, installing..."
    sudo apt-get update
    sudo apt-get install -y patchelf
fi

# Download the file with progress bar
echo "Downloading blockheads_server171.tar.gz..."
curl -#L https://archive.org/download/BHSv171/blockheads_server171.tar.gz -o blockheads_server171.tar.gz

# Extract the file
echo "Extracting blockheads_server171.tar.gz..."
tar xzvf blockheads_server171.tar.gz

# Define variables
FILE="blockheads_server171"
declare -A LIBS=(
    ["libgnustep-base.so.1.24"]="libgnustep-base.so.1.30"
    ["libobjc.so.4.6"]="libobjc.so.4.7"
    ["libgnutls.so.26"]="libgnutls.so.3.7"
    ["libgcrypt.so.11"]="libgcrypt.so.1.10.0"
    ["libxml2.so.2"]="libxml2.so.2"
    ["libffi.so.6"]="libffi.so.3.4"
    ["libnsl.so.1"]="libnsl.so.1"
    ["librt.so.1"]="libnsl.so.1"
    ["libdl.so.2"]="libdl.so.2"
    ["libpthread.so.0"]="libpthread.so.0"
    ["libz.so.1"]="libz.so.1"
    ["libicui18n.so.48"]="libicui18n.so.70.1"
    ["libicuuc.so.48"]="libicuuc.so.70.1"
    ["libicudata.so.48"]="libicudata.so.70.1"
    ["libdispatch.so"]="libdispatch.so.0.1"
    ["libm.so.6"]="libm.so.6"
    ["libstdc++.so.6"]="libstdc++.so.6"
    ["libgcc_s.so.1"]="libgcc_s.so.1"
    ["libc.so.6"]="libc.so.6"
)

# Replace needed libraries with progress feedback
TOTAL_LIBS=${#LIBS[@]}
COUNT=0

for LIB in "${!LIBS[@]}"; do
    COUNT=$((COUNT+1))
    PERCENTAGE=$((COUNT * 100 / TOTAL_LIBS / 5))
    echo -n "Patching $LIB -> ${LIBS[$LIB]} "
    progress_bar $PERCENTAGE
    patchelf --replace-needed $LIB ${LIBS[$LIB]} $FILE || { echo "Failed to patch the BHS for $LIB"; exit 1; }
done

echo -e "\nThe BHS has been patched successfully!"

# Create run.sh with the specified content
cat <<EOF > run.sh
#!/bin/bash

world_id="83cad395edb8d0f1912fec89508d8a1d"
server_port=15151

while true; do
        ./blockheads_server171 -o "\$world_id" -p "\$server_port" >> \$HOME/GNUstep/Library/ApplicationSupport/TheBlockheads/saves/\$world_id/console.log 2>&1
        sleep 1
done
EOF

# Make run.sh executable
chmod +x run.sh

echo -e "\nThe run.sh script has been created and made executable."
