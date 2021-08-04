#!/bin/bash
echo "Welcome to the script that deploy your Website"
git pull --force
echo "Installing python packages"
pip3 install -r ./requirements.txt
echo "Finished Installing python packages"
echo "Installing Node packages"
cd frontend && npm install && npm run build && rm -rf node_modules/ && cd ..
echo "Building Node packages"
echo "Running website"
gcloud app deploy --quiet
echo "Your Website is not Live"
echo "!Remember to do ctrl+shift+r or cmd+shift+r on website tab To see updates!"


