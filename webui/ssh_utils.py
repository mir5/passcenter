import paramiko
import datetime

def ssh_apply_device_password(ip, port, remote_user, remote_password, username, password, valid_time):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=remote_user, password=remote_password)
        print("Login success")

        # Check if the user already exists
        check_user_command = f"id -u {username}"
        stdin, stdout, stderr = client.exec_command(check_user_command)
        user_exists = stdout.channel.recv_exit_status() == 0

        if user_exists:
            print(f"User {username} exists. Updating password, enabling user, and setting expiration date.")
            # Update password
            update_password_command = f"echo '{username}:{password}' | sudo chpasswd"
            stdin, stdout, stderr = client.exec_command(update_password_command)
            print(stdout.read().decode(), stderr.read().decode())

            # Enable user
            enable_user_command = f"sudo usermod -U {username}"
            stdin, stdout, stderr = client.exec_command(enable_user_command)
            print(stdout.read().decode(), stderr.read().decode())

            # Set user expiration date
            expiration_date = valid_time.strftime('%Y-%m-%d')
            set_expiration_command = f"sudo chage -E {expiration_date} {username}"
            stdin, stdout, stderr = client.exec_command(set_expiration_command)
            print(stdout.read().decode(), stderr.read().decode())
        else:
            print(f"User {username} does not exist. Creating user, setting password, granting sudo privileges, and setting expiration date.")
            # Create the new user
            create_user_command = f"sudo useradd -m -p $(openssl passwd -1 {password}) {username}"
            stdin, stdout, stderr = client.exec_command(create_user_command)
            print(stdout.read().decode(), stderr.read().decode())

            # Grant sudo privileges
            grant_sudo_command = f"sudo usermod -aG sudo {username}"
            stdin, stdout, stderr = client.exec_command(grant_sudo_command)
            print(stdout.read().decode(), stderr.read().decode())

            # Set user expiration date
            expiration_date = valid_time.strftime('%Y-%m-%d')
            set_expiration_command = f"sudo chage -E {expiration_date} {username}"
            stdin, stdout, stderr = client.exec_command(set_expiration_command)
            print(stdout.read().decode(), stderr.read().decode())

        client.close()
    except Exception as e:
        print(f"Failed to manage user: {e}")


