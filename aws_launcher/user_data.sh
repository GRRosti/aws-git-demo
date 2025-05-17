#!/bin/bash
# Update system
yum update -y

# Install dependencies
yum install -y git python3

# Clone GitHub repo
git clone https://github.com/GRRosti/aws-git-demo/tree/main/pokemon_game /home/ec2-user/app
cd /home/ec2-user/app

# Install app dependencies (modify based on your app)
pip3 install -r requirements.txt

# Start the app (modify based on your app)
nohup python3 app.py --port {APP_PORT} &

# Set up MOTD (Message of the Day)
cat << 'EOF' > /etc/motd
Welcome to the Application Server!

Usage Instructions:
1. The application is running on port {APP_PORT}.
2. Access it via: http://<server-public-ip>:{APP_PORT}
3. To manage the app:
   - Navigate to /home/ec2-user/app
   - View logs: cat /home/ec2-user/app/nohup.out
   - Restart app: pkill python3 && nohup python3 app.py --port {APP_PORT} &
4. For SSH access, use the key pair provided during setup.
5. Contact support at support@example.com for issues.

Enjoy using the app!
EOF