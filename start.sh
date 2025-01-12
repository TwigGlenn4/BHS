#!/usr/bin/env bash

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

display_progress() {
    clear
    echo "Patching BHS:"
    for LIB in "${!LIBS[@]}"; do
        echo -e "$LIB -> ${LIBS[$LIB]} [${STATUS[$LIB]}]"
    done
}

TOTAL_LIBS=${#LIBS[@]}
COUNT=0
declare -A STATUS

for LIB in "${!LIBS[@]}"; do
    STATUS[$LIB]="Waiting.."
done

display_progress

for LIB in "${!LIBS[@]}"; do
    COUNT=$((COUNT+1))
    STATUS[$LIB]="In Progress!"
    display_progress

    if patchelf --replace-needed $LIB ${LIBS[$LIB]} $FILE; then
        STATUS[$LIB]="Completed!"
    else
        STATUS[$LIB]="Failed"
        echo "There was an issue patching the BHS for $LIB" >&2
        display_progress
        exit 1
    fi

    display_progress
done

echo -e "\nThe BHS has been patched successfully!"
